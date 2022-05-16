from django.contrib import admin

from src.users.models import Organization, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'organization', 'kudos_counter', 'first_name')


class OrgAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrgAdmin)
