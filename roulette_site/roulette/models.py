from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class RouletteBlock(models.Model):
    color = models.CharField(max_length=50, verbose_name='Color')
    multiplication = models.IntegerField(verbose_name='Multiplication')
    chance = models.FloatField(verbose_name='Chance')

    def __str__(self):
        return self.color



class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', null=True)
    color = models.ForeignKey(RouletteBlock, on_delete=models.CASCADE, verbose_name='Color')
    round = models.ForeignKey('Round', on_delete=models.CASCADE, verbose_name='Round')
    time = models.DateTimeField(auto_now_add=True, verbose_name='Time')



class Round(models.Model):
    color = models.CharField(max_length=30, verbose_name='Random color', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', null=True)



class StatisticRouletteUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', null=True)
    bet_value = models.IntegerField(verbose_name='Bet value', null=True)
    win_value = models.IntegerField(verbose_name='Win value', null=True)
    color = models.CharField(max_length=30, verbose_name='Bet color', null=True)
    time = models.DateTimeField(verbose_name='Time', auto_now_add=True, null=True)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    balance = models.IntegerField(verbose_name='Balance', default=0)
    nickname = models.CharField(verbose_name='Nickname', max_length=64)
    photo = models.ImageField(verbose_name='Photo', upload_to='photo/%Y/%m/%d')
    token = models.CharField(verbose_name='User token', max_length=32, null=True)



class TransferTransactions(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name='Time', null=True)
    sender = models.CharField(max_length=255, verbose_name='Sender name')
    recipient = models.CharField(max_length=255, verbose_name='Recipient name')
    value = models.IntegerField(verbose_name='Value of transfer')



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
