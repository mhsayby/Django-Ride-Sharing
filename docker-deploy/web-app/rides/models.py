from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=500, default="pending")

    destination = models.CharField(max_length=50, blank=False)
    arrival_time = models.CharField(max_length=50, blank=False)
    type = models.CharField(max_length=50, blank=True)
    plate = models.CharField(max_length=50, blank=True)
    volume = models.CharField(max_length=30, blank=True)
    special = models.TextField(max_length=500, blank=True)
    driver = models.TextField(max_length=500, default='None')
    sharer = models.TextField(max_length=500, default='None')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
