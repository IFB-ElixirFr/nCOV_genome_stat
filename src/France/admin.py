from django.contrib import admin

from home.admin import admin_site
from France.models import regionsFrance, vaccinFrance


@admin.register(regionsFrance, site=admin_site)
class regionsFranceAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['nom']

    list_display = ('nom', 'code')


@admin.register(vaccinFrance, site=admin_site)
class vaccinFranceAdmin(admin.ModelAdmin):
    save_on_top = True
    autocomplete_fields = ['region']

    list_display = ('date', 'region', 'totalVaccines')
    list_filter = ('date', 'region__nom')

