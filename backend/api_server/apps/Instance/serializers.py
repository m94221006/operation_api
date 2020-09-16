from rest_framework import serializers
from .models import region,instance,isp,status


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model=region
        fields=('id','en_name','ch_name')

class InstanceSerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source='get_region_name')
    isp_name = serializers.ReadOnlyField(source='get_isp_name')
    status_name = serializers.ReadOnlyField(source='get_status_name') 
    class Meta:
        model = instance
        fields=('id','nid','host_name','region_name','isp_name','ch_name','host_ip','status_name')


class ISPSerializer(serializers.ModelSerializer):
    class Meta:
        model=isp
        fields = '__all__'

class InstanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=status
        fields=('id','name')
