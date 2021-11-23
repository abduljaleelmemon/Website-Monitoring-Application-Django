from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField

interval_time = (('15','15'),   
                ('30','30'),
                ('45','45'),
                ('60','59'),
                )

class WebUser(models.Model):

    name = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name.username

class Website(models.Model):
    name = models.CharField(max_length=200)
    URL = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class WebData(models.Model):
    userInfo = models.ForeignKey(WebUser, on_delete=models.CASCADE)
    websiteInfo = models.ForeignKey(Website, on_delete=models.CASCADE)
    interval = models.IntegerField(default=30, choices=interval_time)
    subscription = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.userInfo.name, self.websiteInfo.name)

class MonitorData(models.Model):
    WebInfo = models.ForeignKey(WebData, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return '{} {}'.format(self.WebInfo.userInfo.name, self.WebInfo.websiteInfo.name)

