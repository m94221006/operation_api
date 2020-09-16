from django.db import models, transaction, connection

import logging
logger = logging.getLogger(__name__)

# Create your models here.
class AlertNotifyType(models.Model):
    name = models.CharField(max_length=20)

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'contact_type'


class Alert40x(models.Model):
    cid = models.ForeignKey("customer.CustomerInfo", on_delete=models.CASCADE, db_column='cid')
    threshold = models.FloatField()
    total_bucket = models.IntegerField()
    error_bucket = models.IntegerField()
    alerting = models.BooleanField(default=False)
    interval = models.IntegerField()
    enabled = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.

    def get_by_cid(self, _cid):
        result = Alert40x.objects.raw('SELECT * FROM alert_40x WHERE cid = %s', [_cid])
        return result

    class Meta:
        db_table = 'alert_40x'


class Alert50x(models.Model):
    cid = models.ForeignKey("customer.CustomerInfo", on_delete=models.CASCADE, db_column='cid')
    threshold = models.FloatField()
    total_bucket = models.IntegerField()
    error_bucket = models.IntegerField()
    alerting = models.BooleanField(default=False)
    interval = models.IntegerField()
    enabled = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.

    def get_by_cid(self, _cid):
        result = Alert50x.objects.raw('SELECT * FROM alert_50x WHERE cid = %s', [_cid])
        return result

    class Meta:
        db_table = 'alert_50x'


class AlertNot20030x(models.Model):
    cid = models.ForeignKey("customer.CustomerInfo", on_delete=models.CASCADE, db_column='cid')
    alerting_time = models.FloatField()
    recovery_time = models.FloatField()
    bucket = models.IntegerField()
    history_avg = models.FloatField(default=0)
    alerting = models.BooleanField(default=False)
    interval = models.IntegerField()
    enabled = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.

    def get_by_cid(self, _cid):
        result = AlertNot20030x.objects.raw('SELECT * FROM alert_not_200_30x WHERE cid = %s', [_cid])
        return result

    class Meta:
        db_table = 'alert_not_200_30x'


class LevelDownConfig(models.Model):
    cid = models.ForeignKey('customer.CustomerInfo', on_delete=models.CASCADE, db_column='cid', verbose_name='customer')
    hid = models.IntegerField(blank=True, null=True)
    down_percentage_alert = models.FloatField()
    down_percentage_recovery = models.FloatField()
    bucket = models.IntegerField()
    enabled = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.

    def get_by_cid(self, _cid):
        result = LevelDownConfig.objects.raw('SELECT * FROM level_down_config WHERE cid = %s', [_cid])
        return result

    @transaction.atomic
    def new_config(self, _cid, _hid, _down_alert, _down_recovery, _bucket, _enabled, _monitors_list):
        try:
            with connection.cursor() as cursor:
                # Create config
                LevelDownConfig.objects.create(
                    cid=_cid,
                    hid=_hid,
                    down_percentage_alert=_down_alert,
                    down_percentage_recovery=_down_recovery,
                    bucket=_bucket,
                    enabled=_enabled
                )
                config_id = LevelDownConfig.objects.lastest('id')
                msg_yml = "Create config successful. "

                # Add monitors
                for i in _monitors_list:
                    LevelDownInstance.objects.create(
                        alert_id=config_id,
                        instance_id=i
                    )
                msg_monitor = "Add monitors successful. "
            msg = msg_yml + msg_monitor
            return msg
        except Exception:
            raise

    @transaction.atomic
    def new_config_sql(self, _cid, _hid, _down_alert, _down_recovery, _bucket, _enabled, _monitors_list):
        logger.info('Create LevelDownConfig by sql')
        try:
            with connection.cursor() as cursor:
                # Create config
                cursor.execute('INSERT INTO level_down_config(cid, hid, down_percentage_alert, down_percentage_recovery, bucket, enabled) VALUES(%s, %s, %s, %s, %s, %s);', [_cid, _hid, _down_alert, _down_recovery, _bucket, _enabled])
                cursor.execute('SELECT currval(\'level_down_config_id_seq\');')
                config_id = cursor.fetchone()[0]
                logger.info('Last insert id is {}'.format(config_id))
                msg_config = "Insert level_down_config successful. "
                logger.info(msg_config)

                # Create alert and monitors mapping
                for i in _monitors_list:
                    # cursor.execute('SELECT id FROM "instance" where id={};'.format(i))
                    # instance_exist = cursor.fetchall()
                    cursor.execute('INSERT INTO level_down_instance(alert_id, instance_id) VALUES(%s, %s);', [config_id, i])
                msg_monitor = "Insert level_down_instance successful. "
                logger.info(msg_monitor)

                msg = msg_config + msg_monitor
            return msg
        except Exception:
            raise

    @transaction.atomic
    def update_config_sql(self, _alert_id, _update_dict):
        logger.info('Update LevelDownConfig by sql')
        logger.info('update_dict is {}'.format(_update_dict))
        logger.info('update_dict length is {}'.format(len(_update_dict)))

        update_config_str = ""
        update_monitor_list = []
        for k, v in _update_dict.items():
            if k == "level_down_monitors":
                update_monitor_list = v.split(",")
            else:
                update_config_str = "{}{}={}, ".format(update_config_str, k, str(v))


        logger.info('update_config_str: {}'.format(update_config_str))
        logger.info('update_monitor_list: {}'.format(update_monitor_list))

        msg_config = ""
        msg_monitors = ""
        with connection.cursor() as cursor:
            try:
                # Update config
                if update_config_str:
                    update_config_str = update_config_str[:-2]
                    cursor.execute('UPDATE level_down_config SET {} WHERE id={};'.format(update_config_str, _alert_id))
                    msg_config = "Update config successful. "

                # Update monitors
                if update_monitor_list:
                    cursor.execute('SELECT instance_id FROM level_down_instance where alert_id={};'.format(_alert_id))
                    original_monitors = cursor.fetchall()

                    original_list = [str(y) for x in original_monitors for y in x]
                    logger.info('original_list: {}'.format(original_list))

                    add_set = set(update_monitor_list) - set(original_list)
                    del_set = set(original_list) - set(update_monitor_list)
                    add_list = list(add_set)
                    del_list = list(del_set)
                    logger.info('add_list: {}'.format(add_list))
                    logger.info('del_list: {}'.format(del_list))

                    for a in add_list:
                        cursor.execute('INSERT INTO level_down_instance (alert_id, instance_id) VALUES({}, {});'.format(_alert_id, a))
                    for d in del_list:
                        cursor.execute('DELETE FROM level_down_instance WHERE alert_id={} and instance_id={};'.format(_alert_id, d))
                    msg_monitors = "Update monitors successful. "
                msg = msg_config + msg_monitors
                return msg
            except Exception:
                raise
        

    @transaction.atomic
    def delete_config_sql(self, _alert_id):
        logger.info('Delete LevelDownConfig by sql')

        with connection.cursor() as cursor:
            try:
                # Delete config
                cursor.execute('DELETE FROM level_down_config WHERE id={};'.format(_alert_id))
                msg_config = "Delete config successful. "

                # Delete monitors
                cursor.execute('DELETE FROM level_down_instance WHERE alert_id={};'.format(_alert_id))
                msg_monitors = "Delete monitors successful. "

                msg = msg_config + msg_monitors
                return msg
            except Exception:
                raise

    class Meta:
        db_table = 'level_down_config'


class LevelDownInstance(models.Model):
    alert = models.ForeignKey(LevelDownConfig, on_delete=models.CASCADE, related_name='level_down_monitors')
    instance = models.ForeignKey("Instance.instance", on_delete=models.CASCADE)

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.instance.ch_name

    class Meta:
        db_table = 'level_down_instance'


class LevelRttConfig(models.Model):
    cid = models.ForeignKey('customer.CustomerInfo', on_delete=models.CASCADE, db_column='cid', verbose_name='customer')
    hid = models.IntegerField(blank=True, null=True)
    rtt_percentage_alert = models.FloatField()
    rtt_percentage_recovery = models.FloatField()
    rtt_threshold = models.FloatField()
    bucket = models.IntegerField()
    enabled = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.

    def get_by_cid(self, _cid):
        result = LevelRttConfig.objects.raw('SELECT * FROM level_rtt_config WHERE cid = %s', [_cid])
        return result

    @transaction.atomic
    def new_config_sql(self, _cid, _hid, _alert, _recovery, _threshold, _bucket, _enabled, _monitors_list):
        logger.info('Create LevelRttConfig by sql')
        try:
            with connection.cursor() as cursor:
                # Create config
                cursor.execute('INSERT INTO level_rtt_config(cid, hid, rtt_percentage_alert, rtt_percentage_recovery, rtt_threshold, bucket, enabled) VALUES(%s, %s, %s, %s, %s, %s, %s);', [_cid, _hid, _alert, _recovery, _threshold, _bucket, _enabled])
                cursor.execute('SELECT currval(\'level_rtt_config_id_seq\');')
                config_id = cursor.fetchone()[0]
                logger.info('Last insert id is {}'.format(config_id))
                msg_config = "Insert level_rtt_config successful. "
                logger.info(msg_config)

                # Create alert and monitors mapping
                for i in _monitors_list:
                    cursor.execute('INSERT INTO level_rtt_instance(alert_id, instance_id) VALUES(%s, %s);', [config_id, i])
                msg_monitor = "Insert level_rtt_instance successful. "
                logger.info(msg_monitor)

                msg = msg_config + msg_monitor
            return msg
        except Exception:
            raise

    @transaction.atomic
    def update_config_sql(self, _alert_id, _update_dict):
        logger.info('Update LevelRttConfig by sql')
        logger.info('update_dict is {}'.format(_update_dict))
        logger.info('update_dict length is {}'.format(len(_update_dict)))

        update_config_str = ""
        update_monitor_list = []
        for k, v in _update_dict.items():
            if k == "level_rtt_monitors":
                update_monitor_list = v.split(",")
            else:
                update_config_str = "{}{}={}, ".format(update_config_str, k, str(v))


        logger.info('update_config_str: {}'.format(update_config_str))
        logger.info('update_monitor_list: {}'.format(update_monitor_list))

        msg_config = ""
        msg_monitors = ""
        with connection.cursor() as cursor:
            try:
                # Update config
                if update_config_str:
                    update_config_str = update_config_str[:-2]
                    cursor.execute('UPDATE level_rtt_config SET {} WHERE id={};'.format(update_config_str, _alert_id))
                    msg_config = "Update config successful. "

                # Update monitors
                if update_monitor_list:
                    cursor.execute('SELECT instance_id FROM level_rtt_instance where alert_id={};'.format(_alert_id))
                    original_monitors = cursor.fetchall()

                    original_list = [str(y) for x in original_monitors for y in x]
                    logger.info('original_list: {}'.format(original_list))

                    add_set = set(update_monitor_list) - set(original_list)
                    del_set = set(original_list) - set(update_monitor_list)
                    add_list = list(add_set)
                    del_list = list(del_set)
                    logger.info('add_list: {}'.format(add_list))
                    logger.info('del_list: {}'.format(del_list))

                    for a in add_list:
                        cursor.execute('INSERT INTO level_rtt_instance (alert_id, instance_id) VALUES({}, {});'.format(_alert_id, a))
                    for d in del_list:
                        cursor.execute('DELETE FROM level_rtt_instance WHERE alert_id={} and instance_id={};'.format(_alert_id, d))
                    msg_monitors = "Update monitors successful. "
                msg = msg_config + msg_monitors
                return msg
            except Exception:
                raise

    @transaction.atomic
    def delete_config_sql(self, _alert_id):
        logger.info('Delete LevelRttConfig by sql')

        with connection.cursor() as cursor:
            try:
                # Delete config
                cursor.execute('DELETE FROM level_rtt_config WHERE id={};'.format(_alert_id))
                msg_config = "Delete config successful. "

                # Delete monitors
                cursor.execute('DELETE FROM level_rtt_instance WHERE alert_id={};'.format(_alert_id))
                msg_monitors = "Delete monitors successful. "

                msg = msg_config + msg_monitors
                return msg
            except Exception:
                raise

    class Meta:
        db_table = 'level_rtt_config'


class LevelRttInstance(models.Model):
    alert = models.ForeignKey(LevelRttConfig, on_delete=models.CASCADE, related_name='level_rtt_monitors')
    instance = models.ForeignKey("Instance.instance", on_delete=models.CASCADE)

    def __str__(self):
        return self.instance.ch_name

    objects = models.Manager()  # The default manager.

    class Meta:
        db_table = 'level_rtt_instance'
