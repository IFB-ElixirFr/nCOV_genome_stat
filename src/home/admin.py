from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from home.models import applicationUser, countries


class nCOV_genome_stats(admin.AdminSite):
    site_header = "Administration - nCOV genome stats"


admin_site = nCOV_genome_stats(name='admin')


@admin.register(applicationUser, site=admin_site)
class applicationUserAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['user__username']

    list_display = ('user', 'location', 'position', 'get_username', 'get_firstname', 'get_lastname')

    def get_username(self, obj):
        return obj.user.username

    def get_firstname(self, obj):
        return obj.user.username

    def get_lastname(self, obj):
        return obj.user.username

    get_username.short_description = 'User name'  # Renames column head
    get_firstname.short_description = 'First name'  # Renames column head
    get_lastname.short_description = 'Last name'  # Renames column head



@admin.register(countries, site=admin_site)
class countriesAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['ADMIN']

    list_display = ('ADMIN', 'ISO_A3', 'ISO_A2')

class applicationUserInline(admin.TabularInline):
    model = applicationUser
    extra = 1
    max_num = 1

admin.site.unregister(User)

@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):

    inlines = [applicationUserInline]



admin_site.register(Group)