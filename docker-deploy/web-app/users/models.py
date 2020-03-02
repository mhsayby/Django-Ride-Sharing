from django.db import models
from django.contrib.auth.models import User
from rides.models import Post


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="owner")
    type = models.CharField(max_length=50, blank=False)
    plate = models.CharField(max_length=50, blank=False)
    volume = models.CharField(max_length=30, blank=False)

    search_dest = models.CharField(max_length=50, blank=True)
    search_time = models.CharField(max_length=50, blank=True)
    search_type = models.CharField(max_length=50, blank=True)
    search_volume = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args,**kwargs):
        super(Profile, self).save(*args,**kwargs)



