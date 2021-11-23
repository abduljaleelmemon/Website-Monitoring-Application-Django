from django.db import models
from django.forms import fields
from rest_framework import serializers
from .models import MonitorData, Website, WebUser, WebData

class WebUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebUser
        fields = ('name', 'email')

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ('name', 'URL')

class WebDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebData
        fields = ('userInfo', 'websiteInfo', 'interval', 'subscription')

class MonitorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorData
        fields = ('WebInfo', 'time', 'status')

