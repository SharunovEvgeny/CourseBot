from django.contrib import admin
from django.db import models
from .models import *
@admin.register(Game,Tier,Tournament,Player,Team,BotUser)
class PersonAdmin(admin.ModelAdmin):
    pass