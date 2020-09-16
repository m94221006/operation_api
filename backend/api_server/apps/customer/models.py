from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomerInfo(models.Model):
    name = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)
    max_url_num = models.IntegerField()
    max_monitor_num = models.IntegerField()
    min_interval_num = models.IntegerField()

    # mapping table
    instance = models.ManyToManyField('Instance.instance')

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.name

    def get_by_customer(self, _customer_name):
        result = CustomerInfo.objects.raw('SELECT * FROM customer_info WHERE name = %s', [_customer_name])
        return result

    class Meta:
        db_table = 'customer_info'

class CustomerContact(models.Model):
    cid = models.ForeignKey("customer.CustomerInfo", on_delete=models.CASCADE, db_column='cid')
    recipient_id = models.CharField(max_length=50, db_column='recipient_id')
    type_id = models.ForeignKey("alert.AlertNotifyType", on_delete=models.CASCADE, db_column='type_id')
    subject = models.CharField(max_length=50, default=None, blank=True, null=True)

    objects = models.Manager()  # The default manager.

    class Meta:
        db_table = 'customer_contact'


class UserProfile(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  customer=models.ForeignKey(CustomerInfo,related_name='relate_to_customer',null=True,on_delete=models.CASCADE)
  credential = models.CharField(max_length=50)

  objects = models.Manager()  # The default manager.

  def __str__(self):
      return self.user.username

  def get_user_name(self):
      return self.user.username

  def get_customer(self):
      if self.customer:
         return self.customer.name
      else:
         return ''

  class Meta:
      db_table = 'user_profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


#class CustomerInstance(models.Model):
#     cid = models.ForeignKey("customer.CustomerInfo", on_delete=models.CASCADE)
#     instance = models.ForeignKey("Instance.instance", on_delete=models.CASCADE)
#     enabled = models.BooleanField(default=True)

#     objects = models.Manager()  # The default manager.

#     def __str__(self):
#         return self.cid

#     class Meta:
#         db_table = 'customer_instance'


#class User(models.Model):
#    cid = models.ForeignKey("customer.CustomerInfo", on_delete=models.CASCADE)
#    username = models.CharField(max_length=50)
#    password = models.CharField(max_length=50)
#    credential = models.CharField(max_length=50)
#    enabled = models.BooleanField(default=True)

#    objects = models.Manager()  # The default manager.

#    def __str__(self):
#        return self.username
    
#    class Meta:
#        db_table = 'customer_user'
