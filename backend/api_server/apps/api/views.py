from django.shortcuts import render
from django.db import models, transaction, connection
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, detail_route, list_route
from rest_framework.response import Response
from rest_framework import status, filters, generics

from Instance.models import region, instance,isp,status
from Instance.serializers import RegionSerializer, InstanceSerializer,ISPSerializer,InstanceStatusSerializer

from heartbeat.models import Protocol, Status, HeartbeatConfig, Url, Detail, HeartbeatInstance
from heartbeat.serializers import ProtocolSerializer, StatusSerializer, HeartbeatConfigSerializer, UrlSerializer, DetailSerializer,HeartbeatInstanceSerializer
from customer.models import CustomerInfo,UserProfile,CustomerContact
from customer.serializers import CustomerInfoSerializer,UserProfileSerializer,CustomerContactSerializer

from alert.models import AlertNotifyType,Alert40x, Alert50x, AlertNot20030x, LevelDownConfig, LevelRttConfig
from alert.serializers import AlertNotifyTypeSerializer,Alert40xSerializer, Alert50xSerializer, AlertNot20030xSerializer, LevelDownConfigSerializer, LevelRttConfigSerializer
import logging
logger = logging.getLogger(__name__)


# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = region.objects.all()
    serializer_class = RegionSerializer

class ISPViewSet(viewsets.ModelViewSet):
    queryset = isp.objects.all()
    serializer_class = ISPSerializer

class InstanceStatusViewSet(viewsets.ModelViewSet):
    queryset = status.objects.all()
    serializer_class = InstanceStatusSerializer

class InstanceViewSet(viewsets.ModelViewSet):
    queryset = instance.objects.filter(enabled = True).all()
    serializer_class = InstanceSerializer
    permission_classes = (IsAuthenticated,)
    # /api/instance/raw_sql_query/

    def get_permissions(self):
        if self.action in ('get_by_region',):
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    @list_route(methods=['get'])
    def get_by_region(self, request):
        region = request.query_params.get('region', None)
        item_instance = instance.fun_raw_sql_query(region=region)
        serializer = InstanceSerializer(item_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return instance.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.nid = validated_data.get('nid', instance.nid)
        instance.ch_name = validated_data.get('ch_name', instance.ch_name)
        instance.host_name = validated_data.get('host_name', instance.host_name)
        instance.host_ip = validated_data.get('language', instance.host_ip)
        instance.save()
        return instance

# HeartbeatConfig related
class HeartbeatConfigViewSet(viewsets.ModelViewSet):
    queryset = HeartbeatConfig.objects.all()
    serializer_class = HeartbeatConfigSerializer

    '''
    def create(self, request, *args, **kwargs):
        post_data = request.data
        print(post_data)
        _cid = request.data['cid']
        _protocol = request.data['hb_protocol']
        _tag = request.data['hb_tag']
        _yml = request.data['hb_yml_name']
       # _status = request.data['hb_status']
        _schedule = request.data['schedule']
        _enabled = request.data['enabled']
        _created_by = request.data['created_by']
        _created_time = request.data['created_time']
        _updated_by = request.data['updated_by']
        _updated_time = request.data['updated_time']
        _url = request.data['full_url']
        _detail_key = request.data['detail_key']
        _detail_value = request.data['detail_value']

        with connection.cursor() as _cursor:
            _cursor.execute('SELECT cid_id, hb_yml_name FROM heartbeat_config where cid_id=%s and hb_yml_name=%s;', [_cid, _yml])
            yml_exist = _cursor.fetchone()

        # CREATE
        if not yml_exist:
            try:
                # msg = HeartbeatConfig.new_config(self, _cid, _protocol, _tag, _yml, _status, _schedule, _enabled, _created_by, _created_time, _updated_by, _updated_time, _url, _detail_key, _detail_value)
                msg = HeartbeatConfig.new_config_sql(self, _cid, _protocol, _tag, _yml, _schedule, _enabled, _created_by, _created_time, _updated_by, _updated_time, _url, _detail_key, _detail_value)
                return Response({'msg': msg, 'status_code': 200}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg': str(e), 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # UPDATE
        else:
            print("Redirect to UPDATE process")
            try:
                # msg = HeartbeatConfig.update_config(self, _cid, _tag, _yml, _status, _enabled, _updated_by, _updated_time)
                msg = HeartbeatConfig.update_config_sql(self, _cid, _tag, _yml, _enabled, _updated_by, _updated_time)
                return Response({'msg': msg, 'status_code': 200}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg': str(e), 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        post_data = request.data
        print(post_data)
        _cid = request.data['cid']
        _yml = request.data['hb_yml_name']
        _tag = request.data['hb_tag']
        _status = request.data['hb_status']
        _enabled = request.data['enabled']
        _updated_by = request.data['updated_by']
        _updated_time = request.data['updated_time']
        _url = request.data['full_url']
        _detail_key = request.data['detail_key']
        _detail_value = request.data['detail_value']

        try:
            # msg = HeartbeatConfig.update_config(self, _cid, _tag, _yml, _status, _enabled, _updated_by, _updated_time)
            msg = HeartbeatConfig.update_config_sql(self, _cid, _tag, _yml, _status, _enabled, _updated_by, _updated_time)
            return Response({'msg': msg, 'status_code': 200}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e), 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    '''
    # def get_by_cid(self, request):
    #     pass

    # def get_by_instance_id(self, request):
    #     pass
class HeartbeatByNameViewSet(generics.ListAPIView):
    serializer_class = HeartbeatConfigSerializer

    def get_queryset(self):
        try:
            _customer = self.kwargs['name']
            _cid = CustomerInfo().get_cid(_customer)
            return HeartbeatConfig.objects.filter(cid=_cid)
        except:
            return None
            # msg = "Please enter correct customer name"
            # return Response({'msg': msg, 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)




class HeartbeatInstanceViewSet(viewsets.ModelViewSet):
    queryset = HeartbeatInstance.objects.all()
    serializer_class = HeartbeatInstanceSerializer

'''
    def create(self, request, **kwargs):
        log = Log("lg_operation_api","lg_operation_api_log")
        """
        Create and return a new `Configinstance', given the validated data.
        """
        serializer = HeartbeatInstanceSerializer(data=request.data)
        if serializer.is_valid():
           configinstance = serializer.save()
           #if configinstance:
             ### call node to generate file
           #  htconfigapi =  HeatbeatDeploy(configinstance.heartbeat,configinstance.instance)
           #  result = htconfigapi.Create_yml_file()
           #  if result:
           #     htstatus =  Status.objects.get(name = 'ready')
           #     serializer.save(status = htstatus)                 
           #  log.logger.info("generate file:{}".format(configinstance.id))
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        log = Log("lg_operation_api","lg_operation_api_log")
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        log.logger.info("partial_update")
        confinginstance = self.get_object()
        serializer = HeartbeatInstanceSerializer(confinginstance,data=request.data,partial=True)
        log.logger.info("request.data:{}".format(request.data))          
        if serializer.is_valid():
            changeinstance = serializer.save()
            #### update yml file to node ####
            #log.logger.info("update file:{},{},{},{}".format(changeinstance.id,changeinstance.instance,changeinstance.status,changeinstance.enabled))
            #htconfigapi =  HeatbeatDeploy(changeinstance.heartbeat,changeinstance.instance)
            #if changeinstance.enabled == True:
            #   result = htconfigapi.Create_yml_file()
            #   log.logger.info("Create_yml_file:{}".format(result))
            #   if result:
            #       htstatus =  Status.objects.get(name = 'ready')
            #       changeinstance = serializer.save(status=htstatus)
            #   else:
            #        htstatus =  Status.objects.get(name = 'deploying')
            #        changeinstance = serializer.save(status=htstatus)
            #else:
            #   result = htconfigapi.Delete_yml_file()
            #   log.logger.info("Delete_yml_file:{}".format(result))
            #   if result:
            #       changeinstance = serializer.save(enabled =  False)
            #   else:
            #       changeinstance = serializer.save(enabled =  True)

            log.logger.info("update file:{},{},{},{}".format(changeinstance.id,changeinstance.instance,changeinstance.status,changeinstance.enabled))       
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
'''  
class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer


# class TagViewSet(viewsets.ModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer


# class StatusViewSet(viewsets.ModelViewSet):
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer


class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = HeartbeatInstance
    # def get_by_cid(self, request):
    #     pass
    #
    # def get_by_heartbeat(self, request):
    #     pass
    

# class DetailViewSet(viewsets.ModelViewSet):
    # queryset = Detail.objects.all()
    # serializer_class = DetailSerializer

    # def get_by_hid(self, request):


# Customer related
class CustomerInfoViewSet(viewsets.ModelViewSet):
    queryset = CustomerInfo.objects.all()
    serializer_class = CustomerInfoSerializer

    def create(self, request, *args, **kwargs):
        serializer = CustomerInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=False)
    def info(self, request):
        cus = request.query_params.get('name', None)
        cus_info = CustomerInfo.get_by_customer(None, cus)

        if cus_info:
            serializer = CustomerInfoSerializer(cus_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            msg = "Please enter correct customer name"
            return Response({'msg': msg, 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerByNameViewSet(generics.ListAPIView):
    serializer_class = CustomerInfoSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        #name = self.request.name
        return CustomerInfo.objects.filter(name=name)


class CustomerContactViewSet(viewsets.ModelViewSet):
    queryset = CustomerContact.objects.all()
    serializer_class = CustomerContactSerializer


# Alert related
class AlertNotifyTypeViewSet(viewsets.ModelViewSet):
    queryset = AlertNotifyType.objects.all()
    serializer_class = AlertNotifyTypeSerializer


class Alert40xViewSet(viewsets.ModelViewSet):
    queryset = Alert40x.objects.all()
    serializer_class = Alert40xSerializer

    @action(methods=['get'], detail=False)
    def config(self, request):
        _cid = request.query_params.get('cid', None)
        _alert_config = Alert40x().get_by_cid(_cid)

        if _alert_config:
            serializer = Alert40xSerializer(_alert_config, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            msg = "Please enter correct cid"
            return Response({'msg': msg, 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Alert50xViewSet(viewsets.ModelViewSet):
    queryset = Alert50x.objects.all()
    serializer_class = Alert50xSerializer

    @action(methods=['get'], detail=False)
    def config(self, request):
        _cid = request.query_params.get('cid', None)
        _alert_config = Alert50x().get_by_cid(_cid)

        if _alert_config:
            serializer = Alert50xSerializer(_alert_config, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            msg = "Please enter correct cid"
            return Response({'msg': msg, 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlertNot20030xViewSet(viewsets.ModelViewSet):
    queryset = AlertNot20030x.objects.all()
    serializer_class = AlertNot20030xSerializer

    @action(methods=['get'], detail=False)
    def config(self, request):
        _cid = request.query_params.get('cid', None)
        _alert_config = AlertNot20030x().get_by_cid(_cid)

        if _alert_config:
            serializer = AlertNot20030xSerializer(_alert_config, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            msg = "Please enter correct cid"
            return Response({'msg': msg, 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LevelDownConfigViewSet(viewsets.ModelViewSet):
    queryset = LevelDownConfig.objects.all()
    serializer_class = LevelDownConfigSerializer

    @action(methods=['get'], detail=False)
    def config(self, request):
        _cid = request.query_params.get('cid', None)
        _alert_config = LevelDownConfig().get_by_cid(_cid)

        if _alert_config:
            serializer = LevelDownConfigSerializer(_alert_config, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            msg = "Please enter correct cid"
            return Response({'msg': msg, 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        logger.info('Receive LevelDownConfig POST requset')
        post_data = request.data
        logger.info(post_data)
        _cid = request.data['cid']
        _hid = request.data['hid']
        _down_alert = request.data['down_percentage_alert']
        _down_recovery = request.data['down_percentage_recovery']
        _bucket = request.data['bucket']
        _enabled = request.data['enabled']
        _monitors = request.data['level_down_monitors']

        _monitors_list = _monitors.split(",")
        logger.info("Monitors list: {}".format(_monitors_list))

        if len(_monitors_list) <= 10:
            try:
                # msg = LevelDownConfig().new_config(_cid, _hid, _down_alert, _down_recovery, _bucket, _enabled, _monitors_list)
                msg = LevelDownConfig().new_config_sql(_cid, _hid, _down_alert, _down_recovery, _bucket, _enabled, _monitors_list)
                return Response({'msg': msg, 'status_code': 200}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg': str(e), 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            msg = "Monitors maximum is 10."
            return Response({'msg': msg, 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def update(self,request, *args, **kwargs,):

        logger.info('Receive LevelDownConfig UPDATE request')

        # Get update id
        _id = kwargs.get('pk')
        logger.info('update id is {}'.format(_id))

        # Validate
        valid, valid_msg, update_dict = self.update_validate(_id, request.data)
        logger.info('valid: {}\n valid_msg: {}\n update_dict: {}\n'.format(valid, valid_msg, update_dict))

        # Update
        if valid:
            try:
                msg = LevelDownConfig().update_config_sql(_id, update_dict)
                queryset = self.queryset.filter(id=_id)
                serializer = self.serializer_class(queryset, many=True)
                logger.info({'msg': msg, 'status_code': 200})
                return Response(serializer.data[0], status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg': str(e), 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'msg': valid_msg, 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def update_validate(self, _id, _data):
        logger.info('Start LevelDownConfig UPDATE validation')
        _valid = True
        _msg = ""
        _update_dict = {}

        with connection.cursor() as _cursor:
            _cursor.execute('SELECT id from level_down_config where id=%s;', [_id])
            config_exist = _cursor.fetchone()

        if config_exist:
            allow_items_list = ["down_percentage_alert", "down_percentage_recovery", "bucket", "enabled", "level_down_monitors"]
            update_list = []
            update_dict = {}

            for i in _data:
                if i in allow_items_list:
                    update_list.append(i)
                    update_dict[i] = _data[i]
                else:
                    return False, "Some provided items are not allowed. ", update_dict

            logger.info('update_list is {}'.format(update_list))
            logger.info('update_dict is {}'.format(update_dict))

            if update_list:
                if 'level_down_monitors' in update_list:
                    _monitors = update_dict['level_down_monitors']
                    if len(_monitors.split(",")) <= 10:
                        _valid, _msg, _update_dict = True, "Validation is completed. ", update_dict
                    else:
                        _valid, _msg = False, "Monitors maximum is 10. "
                else:
                    _valid, _msg, _update_dict = True, "Validation is completed. ", update_dict
            elif len(update_list) > 5:
                _valid, _msg = False, "Some provided items is not allowed. "
            else:
                _valid, _msg = False, "No update items provided. "
        else:
            _valid, _msg = False, "Update id is not exist. "

        return _valid, _msg, _update_dict

    def destroy(self, request, *args, **kwargs):
        logger.info('Receive LevelDownConfig DELETE request')

        # Get delete id
        _id = kwargs.get('pk')
        logger.info('delete id is {}'.format(_id))

        # Validate
        valid, valid_msg = self.destroy_validate(_id)
        logger.info('valid: {}\n valid_msg: {}\n'.format(valid, valid_msg))

        # Delete
        if valid:
            try:
                msg = LevelDownConfig().delete_config_sql(_id)
                return Response({'msg': msg, 'status_code': 200}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg': str(e), 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'msg': valid_msg, 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def destroy_validate(self, _id):
        logger.info('Start LevelDownConfig DELETE validation')
        _valid = True
        _msg = ""

        with connection.cursor() as cursor:
            cursor.execute('SELECT id from level_down_config where id=%s;', [_id])
            config_exist = cursor.fetchone()

        if config_exist:
            _valid, _msg = True, "Validation is completed. "
        else:
            _valid, _msg = False, "Delete id is not exist. "

        return _valid, _msg


class LevelRttConfigViewSet(viewsets.ModelViewSet):
    queryset = LevelRttConfig.objects.all()
    serializer_class = LevelRttConfigSerializer

    @action(methods=['get'], detail=False)
    def config(self, request):
        _cid = request.query_params.get('cid', None)
        _alert_config = LevelRttConfig().get_by_cid(_cid)

        if _alert_config:
            serializer = LevelRttConfigSerializer(_alert_config, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            msg = "Please enter correct cid"
            return Response({'msg': msg, 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        logger.info('Receive LevelRttConfig POST request')
        post_data = request.data
        logger.info(post_data)
        _cid = request.data['cid']
        _hid = request.data['hid']
        _alert = request.data['rtt_percentage_alert']
        _recovery = request.data['rtt_percentage_recovery']
        _threshold = request.data['rtt_threshold']
        _bucket = request.data['bucket']
        _enabled = request.data['enabled']
        _monitors = request.data['level_rtt_monitors']

        _monitors_list = _monitors.split(",")
        logger.info("Monitors list: {}".format(_monitors_list))

        if len(_monitors_list) <= 10:
            try:
                msg = LevelRttConfig().new_config_sql(_cid, _hid, _alert, _recovery, _threshold, _bucket, _enabled, _monitors_list)
                return Response({'msg': msg, 'status_code': 200}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg': str(e), 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            msg = "Monitors maximum is 10. "
            return Response({'msg': msg, 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.info('Receive LevelRttConfig UPDATE request')

        # Get update id
        _id = kwargs.get('pk')
        logger.info('update id is {}'.format(_id))

        # Validate
        valid, valid_msg, update_dict = self.update_validate(_id, request.data)
        logger.info('valid: {}\n valid_msg: {}\n update_dict: {}\n'.format(valid, valid_msg, update_dict))

        # Update
        if valid:
            try:
                msg = LevelRttConfig().update_config_sql(_id, update_dict)
                queryset = self.queryset.filter(id=_id)
                serializer = self.serializer_class(queryset, many=True)
                logger.info({'msg': msg, 'status_code': 200})

                return Response(serializer.data[0], status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg': str(e), 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'msg': valid_msg, 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def update_validate(self, _id, _data):
        logger.info('Start LevelRttConfig UPDATE validation')
        _valid = True
        _msg = ""
        _update_dict = {}

        with connection.cursor() as _cursor:
            _cursor.execute('SELECT id from level_rtt_config where id=%s;', [_id])
            config_exist = _cursor.fetchone()

            if config_exist:
                allow_items_list = ["rtt_percentage_alert", "rtt_percentage_recovery", "rtt_threshold", "bucket", "enabled", "level_rtt_monitors"]
                update_list = []
                update_dict = {}

                for i in _data:
                    if i in allow_items_list:
                        update_list.append(i)
                        update_dict[i] = _data[i]
                    else:
                        return False, "Some provided items are not allowed. ", update_dict

                logger.info('update_list is {}'.format(update_list))
                logger.info('update_dict is {}'.format(update_dict))

                if update_list:
                    if 'level_rtt_monitors' in update_list:
                        _monitors = update_dict['level_rtt_monitors']
                        if len(_monitors.split(",")) <= 10:
                            _valid, _msg, _update_dict = True, "Validation is completed. ", update_dict
                        else:
                            _valid, _msg = False, "Monitors maximum is 10. "
                    else:
                        _valid, _msg, _update_dict = True, "Validation is completed. ", update_dict
                elif len(update_list) > 6:
                    _valid, _msg = False, "Some provided items is not allowed. "
                else:
                    _valid, _msg = False, "No update items provided. "
            else:
                _valid, _msg = False, "Update id is not exist. "

            return _valid, _msg, _update_dict

    def destroy(self, request, *args, **kwargs):
        logger.info('Receive LevelRttConfig DELETE request')

        # Get delete id
        _id = kwargs.get('pk')
        logger.info('delete id is {}'.format(_id))

        # Validate
        valid, valid_msg = self.destroy_validate(_id)
        logger.info('valid: {}\n valid_msg: {}\n'.format(valid, valid_msg))

        # Delete
        if valid:
            try:
                msg = LevelRttConfig().delete_config_sql(_id)
                return Response({'msg': msg, 'status_code': 200}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'msg': str(e), 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'msg': valid_msg, 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def destroy_validate(self, _id):
        logger.info('Start LevelRttConfig DELETE validation')
        _valid = True
        _msg = ""

        with connection.cursor() as cursor:
            cursor.execute('SELECT id from level_rtt_config where id=%s;', [_id])
            config_exist = cursor.fetchone()

        if config_exist:
            _valid, _msg = True, "Validation is completed. "
        else:
            _valid, _msg = False, "Delete id is not exist. "

        return _valid, _msg


# class CustomerInstanceViewSet(viewsets.ModelViewSet):
#     queryset = CustomerInstance.objects.all()
#     serializer_class = CustomerInstanceSerializer


# class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer

    # def get_by_cid(self, request):
    #     pass
    
    # def get_by_username(self, request):
    #     pass
