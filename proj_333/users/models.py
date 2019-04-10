from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_name = models.TextField(max_length=None, default = "Jane Doe")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    personal_message = models.TextField(max_length=None, default = "I am excited to meet you")
    matchedMateID = models.PositiveIntegerField(default=0)
    matchedMatePName = models.TextField(max_length=None, default = "John Doe")
    matchedMateImage = models.ImageField(default='default.jpg', upload_to='profile_pics')
    matchedMatePMessage = models.TextField(max_length=None, default = "Meet me please!!!")
    matchedMatePEmail = models.TextField(max_length=None, default = "johndoe@gmail.com")

    def __str__(self):
        return f'{self.user.username} Profile'