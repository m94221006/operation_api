from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from customer.models import CustomerInfo, UserProfile


# Register your models here.
class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "enabled", "max_url_num", "max_monitor_num", "min_interval_num")


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff','related_customer')


    def related_customer(self, instance):
        if instance.userprofile.customer:
           return instance.userprofile.customer.name
        else:
           return ''
        #return instance.userprofile.customer.name


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# class CustomerInstanceAdmin(admin.ModelAdmin):
#     list_display = ("id", "cid", "instance_id", "enabled")


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "cid", "username", "password", "credential", "enabled")

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(CustomerInfo, CustomerInfoAdmin)
# admin.site.register(CustomerInstance)
#admin.site.register(User, UserAdmin)
