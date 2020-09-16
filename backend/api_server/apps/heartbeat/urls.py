from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from heartbeat import views


# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^api/', include(router.urls))
# ]

# urlpatterns = [
#     path('instance_list/', instance_list),
#     path('instance_list/<int:pk>', instance_detail),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)