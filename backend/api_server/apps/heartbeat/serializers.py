from rest_framework import serializers

from .models import Protocol, Status, HeartbeatConfig, Url, Detail,HeartbeatInstance
from customer.models import CustomerInfo
from Instance.models import instance
import datetime
import time
import os
import logging
class Log:
    def __init__(self,log_file_name,log_name):
        self.logfilename = "%s%s.log"%(log_file_name,time.strftime("%Y%m%d%H%M", time.gmtime()))
        self.logname = log_name
        self.logger = self.__set_log()


    def __set_log(self):
        logpath = os.path.join(os.getcwd(), 'log')
        if not os.path.exists(logpath):
            os.makedirs(logpath)
        filepath = os.path.join(logpath, self.logfilename)
        logger = logging.getLogger(self.logname)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler(filepath,encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        logger.addHandler(console)
        return logger
class ProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        # fields = '__all__'
        fields = ('id', 'name')


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         # fields = '__all__'
#         fields = ('id', 'name')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        # fields = '__all__'
        fields = ('id', 'name')


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        #fields = '__all__'
        fields = ('id', 'full_url', 'enabled')

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        #fields = '__all__'
        fields = ('id', 'key', 'value', 'enabled')



class HeartbeatConfigSerializer(serializers.ModelSerializer):
    # customer_name = serializers.ReadOnlyField(source='get_customer_name')
    url_heartbeat = UrlSerializer(many=True)
    detail_heartbeat = DetailSerializer(many=True)
    #url_heartbeat = serializers.StringRelatedField(many=True)
    #detail_heartbeat = serializers.StringRelatedField(many=True)

    class Meta:
        model = HeartbeatConfig
        fields ='__all__'
        #fields = ('id', 'cid', 'hb_protocol', 'hb_tag', 'hb_yml_name', 'schedule', 'enabled', "created_by", "created_time", "updated_by", "updated_time", "url_heartbeat", "detail_heartbeat")
   

    def create(self, validated_data):
        tmp_urls = validated_data.pop('url_heartbeat')
        tmp_details = validated_data.pop('detail_heartbeat')
        tmp_htconfig = HeartbeatConfig.objects.create(**validated_data)
        log = Log("lg_operation_api","lg_operation_api_log")
        log.logger.info(tmp_details)


        if tmp_htconfig:
            if tmp_urls:
                for url in tmp_urls:
                    Url.objects.create(heartbeat=tmp_htconfig, **url)
            if tmp_details:
                for detail in tmp_details:
                    Detail.objects.create(heartbeat=tmp_htconfig, **detail)
        return tmp_htconfig

    def update(self, instance, validated_data):
        tmp_urls = None
        tmp_details = None
        log = Log("lg_operation_api","lg_operation_api_log")
        #print(validated_data)
        log.logger.info(validated_data)
        if 'url_heartbeat' in validated_data:
            tmp_urls = validated_data.get('url_heartbeat')

        if 'detail_heartbeat' in validated_data:
            tmp_details = validated_data.pop('detail_heartbeat')

        instance_urls = (instance.url_heartbeat).all()
        instance_details = (instance.detail_heartbeat).all()
        urls = list(instance_urls)
        details = list(instance_details)

        instance.hb_tag = validated_data.get('hb_tag', instance.hb_tag)
        instance.hb_yml_name = validated_data.get('hb_yml_name', instance.hb_yml_name)
        instance.schedule = validated_data.get('schedule', instance.schedule)
        instance.enabled = validated_data.get('enabled', instance.enabled)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_time = datetime.datetime.now()
        instance.save()
        
        # update job part
        if tmp_urls:
            for tmp_url in tmp_urls:
                tmp_full_url= tmp_url.get('full_url')
                tmp_enabled = tmp_url.get('enabled')
                search_url = Url.objects.filter(heartbeat = instance.id , full_url = tmp_full_url).first()
                if search_url: # update
                    url = urls.pop(0)
                    url.full_url = tmp_url.get('full_url', url.full_url)
                    url.enabled = tmp_url.get('enabled', url.enabled)
                    url.save()
                else: # new 
                    newurl = Url(heartbeat=instance,full_url=tmp_full_url)
                    newurl.save()

                
        if tmp_details:
           for tmp_detail in tmp_details:
               tmp_key= tmp_detail.get('key')
               search_detail = Detail.objects.filter(key = tmp_key)
               if search_detail: # update
                  detail = details.pop(0)
                  detail.value = tmp_detail.get('value', detail.value)
                  detail.enabled = tmp_detail.get('enabled', detail.enabled)
                  detail.save()
               else: # new 
                    tmp_value= tmp_detail.get('value')
                    newdetail = Detail(heartbeat=instance,key=tmp_key,value=tmp_value)
                    newdetail.save()

        
        '''    
            # delete part
            origin_urls = Url.objects.filter(heartbeat__pk = instance.id)
            for origin_url in origin_urls:
                result = [tmp_url for tmp_url in tmp_urls if tmp_url.get('id') == origin_url.id]
                if len(result) == 0: 
                    origin_url.enabled = False
                    origin_url.save()             
            # update part
            for tmp_url in tmp_urls:
                full_url =  tmp_url.get('full_url')
                url_id =  tmp_url.get('id')
                htconfig_id =  tmp_url.get('heartbeat')
                if url_id != 0:
                    url =  Url.objects.get(pk = url_id)
                    if url:
                        if url.full_url!= full_url:
                            url.full_url = full_url
                            url.save()
                else:
                     Url.objects.create(heartbeat=instance,full_url=hosturls)

        # update job detail
        if tmp_details:
            for tmp_detail in tmp_details:
                key =  tmp_detail.get('key')
                value = tmp_detail.get('value')
                detail_id =  tmp_detail.get('id')
                detail =  Detail.objects.get(pk = detail_id)
                if detail:
                    if detail.key != key:
                        detail.key = key
                    if detail.value != value:
                        detail.value = value
                    detail.save()
        '''
        return instance           

        # def validate_cid(self, cid):
        #     check_cid = CustomerInfo.objects.filter(cid__exact = cid)
        #     print(check_cid)
        #     if not check_cid:
        #         msg = 'Cid %s is not exist.' %cid
        #         raise ValidationError(detail=msg)
        #     return cid
        
        # def validate_instance(self, instance):
        #     check_instance = instance.objects.filter(ch_name_exact = instance)
        #     CustomerInfo.objects.filter(cid__exact = cid)
        #     if not check_instance:
        #         msg = 'iInstance %s is not exist.' %cid
        #         raise ValidationError(detail=msg)
        #     return cid



class HeartbeatInstanceSerializer(serializers.ModelSerializer):
     class Meta:
         model = HeartbeatInstance
         fields = '__all__'
         #fields = ('id', 'heartbeat', 'instance')
