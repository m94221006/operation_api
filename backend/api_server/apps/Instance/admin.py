from django.contrib import admin
from Instance.models import region,isp,status,instance

# Register your models here.
class regionAdmin(admin.ModelAdmin):
    list_display = ("id","en_name","ch_name")


class instanceAdmin(admin.ModelAdmin):
    list_display = ("nid","region_name","isp_name","name_item","host_ip","status_name",'i_vip','enabled','created_time')
    list_filter=('instance_region__ch_name','instance_isp__name','instance_status__name','enabled')
    search_fields = ('ch_name',)
    list_editable = ( 'i_vip', 'enabled')

    def name_item(self, obj):
        return obj.host_name+":"+obj.ch_name

    def region_name(self,obj):
        return obj.instance_region.ch_name

    def isp_name(self,obj):
        return obj.instance_isp.name
    
    def status_name(self,obj):
        return obj.instance_status.name


admin.site.register(region,regionAdmin)
admin.site.register(isp)
admin.site.register(status)
admin.site.register(instance,instanceAdmin)