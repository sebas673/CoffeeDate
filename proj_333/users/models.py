from django.db import models
from django.contrib.auth.models import User
# from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    personal_message = models.TextField(max_length=None, default="Hello!")
    match_mate_ID = models.PositiveIntegerField(default=0)
    signed_in = models.BooleanField(default=True)
    is_matched = models.BooleanField(default=False)

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
