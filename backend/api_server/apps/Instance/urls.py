from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import instance_list,instance_detail
from django.urls import path

urlpatterns = [
    path('instance_list/', instance_list),
    path('instance_list/<int:pk>', instance_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)