from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Prefs(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True)
    pref1 = models.IntegerField(default=3, validators=[MaxValueValidator(5), MinValueValidator(1)])
    pref2 = models.IntegerField(default=3, validators=[MaxValueValidator(5), MinValueValidator(1)])
    pref3 = models.IntegerField(default=3, validators=[MaxValueValidator(5), MinValueValidator(1)])
    pref4 = models.IntegerField(default=3, validators=[MaxValueValidator(5), MinValueValidator(1)])
    pref5 = models.IntegerField(default=3, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return f'{self.user.Profile.first_name} Prefs'

    def get_absolute_url(self):
        return reverse('prefs-detail', kwargs={'pk': self.pk})

class Profile(models.Model):

    user = models.OneToOneField(get_user_model(), related_name='Profile', on_delete=models.CASCADE, null=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    personal_message = models.TextField(max_length=None, default="Hello!")

    signed_in = models.BooleanField(default=True)  # this one will never change
    is_matched = models.BooleanField(default=False)  # does the user have a match?
    has_customized = models.BooleanField(default=False)  # has the user customized their preferences?

    mate_ID = models.PositiveIntegerField(default=0)
    mate_firstname = models.CharField(max_length=50, default="Christoper")
    mate_lastname = models.CharField(max_length=50, default="Eisgruber")
    mate_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    mate_personal_message = models.TextField(max_length=None, default="Hello!")
    mate_email = models.CharField(max_length=50, default="princeton@princeton.edu")



    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # have to find a way to do this with aws S3
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
