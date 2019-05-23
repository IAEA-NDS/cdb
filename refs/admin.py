from django.contrib import admin
from .models import Ref

class RefAdmin(admin.ModelAdmin):
    search_fields = ('authors', 'title', 'journal')
admin.site.register(Ref, RefAdmin)
