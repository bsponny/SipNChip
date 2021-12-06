from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    userType = models.IntegerField(default=1) #1 = Player, 2 = Sponsor, 3 = Bartender, 4 = Manager, 5 = Admin
    currentHole = models.IntegerField(default=0)
    triedToSponsor = models.BooleanField(default=False)
    triedToOrder = models.BooleanField(default=False)


    @receiver(post_save, sender=User)
    def create_account(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance, balance=0.00, userType=1)

    @receiver(post_save, sender=User)
    def save_account(sender, instance, **kwargs):
        instance.account.save()

    def __str__(self):
        return str(self.user.username) + " has $" + str(self.balance) + " userType: " + str(self.userType) + " id: " + str(self.id)

class Tournament(models.Model):
    dayOfTournament = models.DateField()
    playersRegistered = models.ManyToManyField(User, related_name="players", blank=True)
    sponsoredBy = models.ManyToManyField(User, related_name="sponsors", blank=True)
    leaderboard = models.JSONField(default=dict)
    isOpen = models.BooleanField(default=False)
    def __str__(self):
        return str(self.dayOfTournament)

class SponsorRequest(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dayOfTournament = models.DateField(null=True)

class Drink(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return str(self.name)

class DrinkOrder(models.Model):
    drinks = models.JSONField(default=dict)
    orderedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    totalPrice = models.DecimalField(max_digits=5, decimal_places=2, null=True)

class Scorecard(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=True)
    scores = models.JSONField(default=dict)
    finished = models.BooleanField(default=False)

class OrderNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    message = models.CharField(max_length=100)
