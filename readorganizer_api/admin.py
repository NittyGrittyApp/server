from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from readorganizer_api import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Channel)
admin.site.register(models.ChannelFeed)
admin.site.register(models.Entry)
admin.site.register(models.EntryContent)
admin.site.register(models.EntryNote)
admin.site.register(models.ChannelTag)
admin.site.register(models.EntryTag)