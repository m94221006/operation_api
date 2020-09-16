from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (RegionViewSet,ISPViewSet,InstanceStatusViewSet, InstanceViewSet, HeartbeatConfigViewSet, 
                    CustomerInfoViewSet, UrlViewSet,HeartbeatInstanceViewSet,
                    UserProfileViewSet,ProtocolViewSet, CustomerContactViewSet, 
                    AlertNotifyTypeViewSet,Alert40xViewSet, Alert50xViewSet, AlertNot20030xViewSet, 
                    LevelDownConfigViewSet, LevelRttConfigViewSet)

from .views import CustomerByNameViewSet, HeartbeatByNameViewSet



router = DefaultRouter()
router.register(r'region', RegionViewSet, base_name='regions')
router.register(r'isp', ISPViewSet, base_name='isps')
router.register(r'instancestatus', InstanceStatusViewSet, base_name='instancestatuss')
router.register(r'instance', InstanceViewSet, base_name='instances')
router.register(r'protocol', ProtocolViewSet, base_name='protocols')
router.register(r'heartbeat', HeartbeatConfigViewSet, base_name='heartbeat')
router.register(r'heartbeat-instance', HeartbeatInstanceViewSet, base_name='heartbeatinstance')
router.register(r'customer', CustomerInfoViewSet, base_name='customer')
router.register(r'customer-contact', CustomerContactViewSet, base_name='customer-contact')
router.register(r'userprofile', UserProfileViewSet, base_name='userprofile')
#router.register(r'url', UrlViewSet, base_name='url')
router.register(r'alert/notify-type', AlertNotifyTypeViewSet, base_name='alert-notify-type')
router.register(r'alert/40x', Alert40xViewSet, base_name='alert_40x')
router.register(r'alert/50x', Alert50xViewSet, base_name='alert_50x')
router.register(r'alert/not20030x', AlertNot20030xViewSet, base_name='alert_not20030x')
router.register(r'alert/level-down', LevelDownConfigViewSet, base_name='alert_level_down')
router.register(r'alert/level-rtt', LevelRttConfigViewSet, base_name='alert_level_rtt')


urlpatterns = [
    url(r'^', include(router.urls)),
    url('^heartbeat/name/(?P<name>.+)/$', HeartbeatByNameViewSet.as_view()),
    url('^customer/name/(?P<name>.+)/$', CustomerByNameViewSet.as_view()),
]
