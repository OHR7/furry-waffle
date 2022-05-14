from django.contrib import admin

from src.kudos.models import Kudo


class KudosAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'date')


admin.site.register(Kudo, KudosAdmin)
