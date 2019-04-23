from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils import timezone


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    group_image = models.ImageField(default='default.jpg', upload_to='group_pics')
    date_created = models.DateTimeField(default=timezone.now)
    group_description = models.TextField()
    delete_me = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # on_delete=models.CASCADE means this group will be deleted when the owner us deleted
    # members = ArrayField(models.PositiveIntegerField(default=0), blank=True)

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('group-detail', kwargs={'pk': self.pk})
