from django.db import models, transaction, connection


# Create your models here.
class Protocol(models.Model):
    name = models.CharField(max_length=50)

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'heartbeat_protocol'


# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#
#     objects = models.Manager()  # The default manager.
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table = 'heartbeat_tag'


class Status(models.Model):
    name = models.CharField(max_length=50)

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'heartbeat_status'


class HeartbeatConfig(models.Model):
    cid = models.ForeignKey('customer.CustomerInfo', on_delete=models.CASCADE, verbose_name='customer',db_column='cid')
    hb_protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    hb_tag = models.TextField(default=None, blank=True, null=True)
    hb_yml_name = models.CharField(max_length=50)
    schedule = models.IntegerField(default=120)
    origin = models.CharField(max_length=100,default="", blank=True)
    enabled = models.BooleanField(default=True)
    created_by= models.CharField(max_length =50,default="system")
    #created_by = models.ForeignKey('customer.User', on_delete=models.CASCADE, related_name='created_by_set', null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length =50,default="system")
    #updated_by = models.ForeignKey('customer.User', on_delete=models.CASCADE, related_name='updated_by_set', null=True)
    updated_by = models.CharField(max_length =50,default="system")
    updated_time = models.DateTimeField(auto_now=True)

    # mapping table
    #instances = models.ManyToManyField('Instance.instance', through='ConfigInstance')

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.hb_yml_name

    @transaction.atomic
    def new_config(self, _cid, _protocol, _tag, _yml, _schedule, _enabled, _created_by, _created_time, _updated_by, _updated_time, _url, _detail_key, _detail_value):
        try:
            with connection.cursor() as cursor:
                # Create yml
                print("CREATE YML")
                HeartbeatConfig.objects.create(
                    cid=_cid,
                    hb_protocol=_protocol,
                    hb_tag=_tag,
                    hb_yml_name=_yml,
                    schedule=_schedule,
                    enabled=_enabled,
                    created_by=_created_by,
                    updated_by=_created_time
                )
                cursor.execute('SELECT id FROM heartbeat_config where cid_id=%s and hb_yml_name=%s;', [_cid, _yml])
                hb_id = (cursor.fetchone())[0]
                msg_yml = "Create heartbeat config successful. "

                # Add URL
                print("ADD URLS")
                new_url = _url.split(",")
                for i in new_url:
                    Url.objects.create(
                        full_url=i,
                        heartbeat_id=hb_id,
                        enabled=_enabled
                    )
                msg_url = "Add URLs successful. "

                # Add detail
                if _detail_key and _detail_value:
                    Detail.objects.create(
                        key=_detail_key,
                        value=_detail_value,
                        enabled=_enabled,
                        heartbeat_id=hb_id
                    )
                    msg_detail = "Add detail successful. "
                else:
                    msg_detail = "Detail key or value is not provided. "

                msg = msg_yml + msg_url + msg_detail
            return msg
        except Exception:
            raise

    @transaction.atomic
    def new_config_sql(self, _cid, _protocol, _tag, _yml, _schedule, _enabled, _created_by, _created_time, _updated_by, _updated_time, _url, _detail_key, _detail_value):
        try:
            with connection.cursor() as cursor:
                # Create yml
                print("CREATE YML")
                cursor.execute('INSERT INTO heartbeat_config(cid_id, hb_protocol_id, hb_tag, hb_yml_name, schedule, enabled, created_by_id, created_time, updated_by_id, updated_time) VALUES(%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, CURRENT_TIMESTAMP)', [_cid, _protocol, _tag, _yml, _schedule, _enabled, _created_by, _updated_by])
                cursor.execute('SELECT id FROM heartbeat_config where cid_id=%s and hb_yml_name=%s;', [_cid, _yml])
                hb_id = (cursor.fetchone())[0]
                msg_yml = "Create heartbeat config successful. "

                # Add URL
                print("ADD URLS")
                new_url = _url.split(",")
                for i in new_url:
                    cursor.execute('INSERT INTO heartbeat_url(full_url, enabled, heartbeat_id)VALUES(%s, %s, %s)', [i, _enabled, hb_id])
                msg_url = "Add URLs successful. "

                # Add detail
                if _detail_key and _detail_value:
                    cursor.execute('INSERT INTO heartbeat_detail(key, value, enabled, heartbeat_id)VALUES(%s, %s, %s, %s)', [_detail_key, _detail_value, _enabled, hb_id])
                    msg_detail = "Add detail successful. "
                    print("ADD DETAIL")
                else:
                    msg_detail = "Detail key or value is not provided. "

                msg = msg_yml + msg_url + msg_detail
            return msg
        except Exception:
            raise

    @transaction.atomic
    def update_config(self, _cid, _tag, _yml, _enabled, _updated_by, _updated_time):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id FROM heartbeat_config where cid_id=%s and hb_yml_name=%s;', [_cid, _yml])
                hb_id = (cursor.fetchone())[0]

                if hb_id:
                    # Update yml
                    if _tag:
                        HeartbeatConfig.objects.filter(id=hb_id).update(hb_tag=_tag)
                    elif _enabled:
                        HeartbeatConfig.objects.filter(id=hb_id).update(enabled=_enabled)
                    elif _updated_by:
                        HeartbeatConfig.objects.filter(id=hb_id).update(updated_by_id=_updated_by)
                    else:
                        msg_yml = "No item provided for update. "
                else:
                    msg_yml = "Customer yml is not exist. "
            return msg_yml
        except Exception:
            raise

    @transaction.atomic
    def update_config_sql(self, _cid, _tag, _yml, _enabled, _updated_by, _updated_time):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id FROM heartbeat_config where cid_id=%s and hb_yml_name=%s;', [_cid, _yml])
                hb_id = (cursor.fetchone())[0]

                if hb_id:
                    # Update yml
                    if _tag or _enabled or _updated_by:
                        yml_update_str = ""
                        yml_update_dict = {'hb_tag': "\'" + _tag + "\'", 'enabled': _enabled, 'updated_by_id': _updated_by}
                        for k, v in yml_update_dict.items():
                            if v:
                                yml_update_str = yml_update_str + k + "=" + v + ", "
                        yml_update_str_final = yml_update_str[:-2]
                        cursor.execute('UPDATE heartbeat_config SET updated_time=CURRENT_TIMESTAMP, {} where cid_id={} and hb_yml_name=\'{}\';'.format(yml_update_str_final, _cid, _yml))
                        msg_yml = "Update yml success. "
                    else:
                        msg_yml = "No item provided for update. "
                else:
                    msg_yml = "Customer yml is not exist. "
            return msg_yml
        except Exception:
            raise

    class Meta:
        db_table = 'heartbeat_config'


class HeartbeatInstance(models.Model):
    heartbeat = models.ForeignKey(HeartbeatConfig, on_delete=models.CASCADE)
    instance = models.ForeignKey("Instance.instance", on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.heartbeat.hb_yml_name

    class Meta:
        db_table = 'heartbeat_instance'


class Url(models.Model):
    full_url = models.CharField(max_length=300)
    heartbeat = models.ForeignKey(HeartbeatConfig, on_delete=models.CASCADE, related_name='url_heartbeat', db_column='hid')
    enabled = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.full_url

    class Meta:
        db_table = 'heartbeat_url'


class Detail(models.Model):
    heartbeat = models.ForeignKey(HeartbeatConfig, on_delete=models.CASCADE, related_name='detail_heartbeat', db_column='hid')
    key = models.TextField(default=None, blank=True, null=True)
    value = models.TextField(default=None, blank=True, null=True)
    enabled = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return str(self.key) + ": " + str(self.value)

    class Meta:
        db_table = 'heartbeat_detail'



