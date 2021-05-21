from django.db import models

# Create your models here.


class Post(models.Model):
    post = models.JSONField()
    channel = models.CharField(max_length=50)
    published = models.CharField(max_length=1, default='N')
