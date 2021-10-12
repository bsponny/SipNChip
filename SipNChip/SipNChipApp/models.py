from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal


# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)
    userType = models.IntegerField(default = 1) #1 = Player, 2 = Sponsor, 3 = Bartender, 4 = Manager


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance, balance=0.00, userType=1)


@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    instance.account.save()

def __str__(self):
        return self.user
