from django.contrib import admin
from api.models import DrugsAndSNP

class DrugsAdmin(admin.ModelAdmin):
    list_display = ['drug', 'snp']

admin.site.register(DrugsAndSNP, DrugsAdmin)