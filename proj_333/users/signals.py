from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import random

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # numUsers = User.objects.all().last()
    # rNumber = random.randint(1, 4)
    # instance.profile.matchedMateID = rNumber
    # instance.profile.matchedMatePName = User.objects.get(id=rNumber).profile.preferred_name
    # instance.profile.matchedMatePMessage = User.objects.get(id=rNumber).profile.personal_message
    # instance.profile.matchedMateImage = User.objects.get(id=rNumber).profile.image
    # instance.profile.matchedMatePEmail = User.objects.get(id=rNumber).email
    instance.profile.save()