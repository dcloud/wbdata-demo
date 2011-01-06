from django.contrib import admin
from wbdata.models import *

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ['name']

admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Country)


class DataPointAdmin(admin.ModelAdmin):
    list_display = ('indicator', 'year', 'country')

admin.site.register(DataPoint, DataPointAdmin)
