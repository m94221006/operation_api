from django.contrib import admin
from heartbeat.models import Protocol, Status, HeartbeatConfig, Url, Detail, HeartbeatInstance

# Register your models here.
# class ProtocolAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")


# class TagAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")


class StatusAdmin(admin.ModelAdmin):
     list_display = ("id", "name")

class HeartbeatConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "cid", "hb_protocol", "hb_tag", "hb_yml_name", "schedule", "enabled", "created_by", "created_time", "updated_by", "updated_time")


class UrlAdmin(admin.ModelAdmin):
    list_display = ("id", "full_url", "heartbeat", "enabled")


class DetailAdmin(admin.ModelAdmin):
    list_display = ("id", "heartbeat", "key", "value", "enabled")


class HeartbeatInstanceAdmin(admin.ModelAdmin):
    list_display = ("id", "heartbeat", "instance",'status',"instance_item","status_item", "enabled")
    list_filter=('heartbeat','status','enabled',)
    search_fields = ('heartbeat','instance',)
    list_editable = ( 'status', 'enabled')
    def status_item(self, obj):
        return str(obj.status.id)+":"+obj.status.name

    def instance_item(self,obj):
        return str(obj.instance.id)+":"+obj.instance.host_name+":"+obj.instance.host_ip


admin.site.register(Protocol)
admin.site.register(Status,StatusAdmin)
admin.site.register(HeartbeatConfig, HeartbeatConfigAdmin)
admin.site.register(Url, UrlAdmin)
admin.site.register(Detail, DetailAdmin)
admin.site.register(HeartbeatInstance,HeartbeatInstanceAdmin)
 
