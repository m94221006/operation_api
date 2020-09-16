from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CustomerInfo,UserProfile,CustomerContact

class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = '__all__'
        #fields = ('id', 'name', 'enabled', 'max_url_num', 'max_monitor_num', 'min_interval_num','instances')

    # def validate_cid(self, cid):
    #     check_cid = CustomerInfo.objects.filter(cid__exact=cid)
    #     print(check_cid)
    #     if check_cid:
    #         msg = 'Cid %s is already exist.' % cid
    #         raise ValidationError(detail=msg)
    #     return cid

    def validate_name(self, name):
        check_name = CustomerInfo.objects.filter(name__exact=name)
        print(check_name)
        if check_name:
            msg = 'Customer %s is already exist.' % name
            raise ValidationError(detail=msg)
        return name


class CustomerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContact
        fields = ('id', 'cid', 'recipient_id', 'type_id', 'subject')


class UserProfileSerializer(serializers.ModelSerializer):
    #customer = CustomerInfoSerializer()
    customer_name = serializers.ReadOnlyField(source='get_customer')
    user_name = serializers.ReadOnlyField(source='get_user_name')    
    class Meta:
        model = UserProfile
        #fields = '__all__'
        fields = ('id','customer' ,'customer_name','user', 'user_name','credential')
# class CustomerInstanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomerInstance
#         # fields = '__all__'
#         fields = ('id', 'cid', 'instance', 'enabled')


#class UserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = User
        # fields = '__all__'
#        fields = ('id', 'cid', 'username', 'password', 'credential', 'enabled')
