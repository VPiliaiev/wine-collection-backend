from django.contrib import admin

from wine.models import WineType, Category, Mood, Country, Wine, Purpose

admin.site.register(WineType)
admin.site.register(Category)
admin.site.register(Mood)
admin.site.register(Country)
admin.site.register(Wine)
admin.site.register(Purpose)
