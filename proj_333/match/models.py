from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from users.models import Profile


class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # on_delete=models.CASCADE means this group will be deleted when the owner us deleted
    group_name = models.CharField(max_length=100)
    group_image = models.ImageField(default='default.jpg', upload_to='group_pics')
    date_created = models.DateTimeField(default=timezone.now)
    group_description = models.TextField()
    members = models.ManyToManyField(Profile)

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('group-detail', kwargs={'pk': self.pk})


class Pair(models.Model):
    pair_1 = models.PositiveIntegerField(default=0)
    pair_1_first = models.CharField(max_length=50, null=True)
    pair_1_last = models.CharField(max_length=50, null=True)
    pair_2 = models.PositiveIntegerField(default=0)
    pair_2_first = models.CharField(max_length=50, null=True)
    pair_2_last = models.CharField(max_length=50, null=True)

    pair_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.pair_1} & {self.pair_2} in "{self.pair_group}" Pair'
