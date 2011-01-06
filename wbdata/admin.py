from django.contrib import admin
from wbdata.models import *

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ['name']

admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Country)
admin.site.register(DataPoint)
