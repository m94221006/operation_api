from rest_framework import serializers

from .models import (AlertNotifyType, Alert40x, Alert50x,
                     AlertNot20030x, LevelDownConfig, LevelRttConfig)

class AlertNotifyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertNotifyType
        fields = ('id', 'name')



class Alert40xSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert40x
        fields = ('id', 'cid', 'threshold', 'total_bucket', 'error_bucket', 'alerting', 'interval', 'enabled')


class Alert50xSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert50x
        fields = ('id', 'cid', 'threshold', 'total_bucket', 'error_bucket', 'alerting', 'interval', 'enabled')


class AlertNot20030xSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertNot20030x
        fields = ('id', 'cid', 'alerting_time', 'recovery_time', 'bucket', 'history_avg', 'alerting', 'interval', 'enabled')


class LevelDownConfigSerializer(serializers.ModelSerializer):
    level_down_monitors = serializers.StringRelatedField(many=True)

    class Meta:
        model = LevelDownConfig
        fields = ('id', 'cid', 'hid', 'down_percentage_alert', 'down_percentage_recovery', 'bucket', 'enabled', 'level_down_monitors')


class LevelRttConfigSerializer(serializers.ModelSerializer):
    level_rtt_monitors = serializers.StringRelatedField(many=True)

    class Meta:
        model = LevelRttConfig
        fields = ('id', 'cid', 'hid', 'rtt_percentage_alert', 'rtt_percentage_recovery', 'rtt_threshold', 'bucket', 'enabled', 'level_rtt_monitors')
