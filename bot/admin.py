from django.contrib import admin
from django.db import models
from .models import *
@admin.register(Game,Tournament,Player,Team,BotUser,GameNow)
class PersonAdmin(admin.ModelAdmin):
    pass