from django.contrib import admin
from .models import Fitting
from .models import FittingNeck


@admin.register(Fitting)
class FittingModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(FittingNeck)
class FittingNeckModelAdmin(admin.ModelAdmin):
    list_display = ('fitting',)
