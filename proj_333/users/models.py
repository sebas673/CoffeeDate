from django.db import models
from django.contrib.auth.models import User
# from PIL import Image


class Profile(models.Model):
    # REQUIRED_FIELDS = ('user',)

    user = models.OneToOneField(User, related_name='Profile', on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    personal_message = models.TextField(max_length=None, default="Hello!")
    signed_in = models.BooleanField(default=True)
    is_matched = models.BooleanField(default=False)

    mate_ID = models.PositiveIntegerField(default=0)
    mate_firstname = models.CharField(max_length=50, default="Christoper")
    mate_lastname = models.CharField(max_length=50, default="Eisgruber")
    mate_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    mate_personal_message = models.TextField(max_length=None, default="Hello!")
    mate_email = models.TextField(max_length=None, default="princeton@princeton.edu")

    def __str__(self):
        return f'{self.user.username} Profile'

    # have to find a way to do this with aws S3
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
