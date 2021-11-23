from django.contrib import admin
from monitor_app import models

# Register your models here.
from .models import MonitorData, Website, WebUser, WebData

admin.site.register(MonitorData)
admin.site.register(WebData)
admin.site.register(Website)
admin.site.register(WebUser)
