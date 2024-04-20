from django.contrib import admin

from data_loss_prevention.models import CaughtMessage, Pattern

admin.site.register(Pattern)
admin.site.register(CaughtMessage)
