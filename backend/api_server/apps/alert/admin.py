from django.contrib import admin
from alert.models import (Alert40x, Alert50x, AlertNot20030x,
                          LevelDownConfig, LevelDownInstance, LevelRttConfig, LevelRttInstance)


# Register your models here.
# class AlertCustomerAdmin(admin.ModelAdmin):
#     list_display = ("id", "cid", "recipient_id", "type_id", "subject")


class Alert40xAdmin(admin.ModelAdmin):
    list_display = ("id", "cid", "threshold", "total_bucket", "error_bucket", "alerting", "interval", "enabled")


class Alert50xAdmin(admin.ModelAdmin):
    list_display = ("id", "cid", "threshold", "total_bucket", "error_bucket", "alerting", "interval", "enabled")


class AlertNot20030xAdmin(admin.ModelAdmin):
    list_display = ("id", "cid", "alerting_time", "recovery_time", "bucket", "history_avg", "alerting", "interval", "enabled")


class LevelDownConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "cid", "hid", "down_percentage_alert", "down_percentage_recovery", "bucket", "enabled")


class LevelDownInstanceAdmin(admin.ModelAdmin):
    list_display = ("id", "alert", "instance")


class LevelRttConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "cid", "hid", "rtt_percentage_alert", "rtt_percentage_recovery", "rtt_threshold", "bucket", "enabled")


class LevelRttInstanceAdmin(admin.ModelAdmin):
    list_display = ("id", "alert", "instance")


admin.site.register(Alert40x, Alert40xAdmin)
admin.site.register(Alert50x, Alert50xAdmin)
admin.site.register(AlertNot20030x, AlertNot20030xAdmin)
admin.site.register(LevelDownConfig, LevelDownConfigAdmin)
admin.site.register(LevelDownInstance, LevelDownInstanceAdmin)
admin.site.register(LevelRttConfig, LevelRttConfigAdmin)
admin.site.register(LevelRttInstance, LevelRttInstanceAdmin)
#admin.site.register(AlertNotifyType)


