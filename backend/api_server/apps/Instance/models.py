from django.db import models


# Create your models here.
class region(models.Model):
    en_name = models.CharField(max_length=100)
    ch_name = models.CharField(max_length=200,default ='')

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.ch_name


class status(models.Model):
    name = models.CharField(max_length=30)
    deleted = models.BooleanField(default = False)

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.name


class isp(models.Model):
    name = models.CharField(max_length=100)
    deleted = models.BooleanField(default = False)

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.name


class instance(models.Model):
    instance_status = models.ForeignKey(status, on_delete=models.CASCADE, null=True)
    instance_region = models.ForeignKey(region, on_delete=models.CASCADE, null=True)
    instance_isp = models.ForeignKey(isp, on_delete=models.CASCADE, null=True)
    nid = models.CharField(max_length=100)
    ch_name = models.CharField(max_length=300, default='')
    host_name = models.CharField(max_length=100)
    host_ip = models.GenericIPAddressField(default='0.0.0.0')
    i_vip = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    creator = models.CharField(max_length=50, default="system")
    created_time = models.DateTimeField(auto_now_add=True)
    lastupdatedby = models.CharField(max_length=50, default="system")
    lastupdatedtime = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.ch_name

    def get_region_name(self):
        return self.instance_region.ch_name

    def get_isp_name(self):
        return self.instance_isp.name

    def get_status_name(self):
        return self.instance_status.name

    def fun_raw_sql_query(**kwargs):
        region_name = kwargs.get('region')

        if region_name:
            region_id=region.objects.get(ch_name=region_name).pk
            result = instance.objects.raw('SELECT * FROM instance WHERE instance.instance_region_id = %s', [region_id])
        else:
            result = instance.objects.raw('SELECT * FROM instance')
        return result

    class Meta:
          db_table='instance'










