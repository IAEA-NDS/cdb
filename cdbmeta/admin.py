from django.contrib import admin

from .models import (Attribution, LatticeParameters, Material,
                     CDBRecord, Potential)

admin.site.register(Attribution)
admin.site.register(LatticeParameters)
admin.site.register(Material)
admin.site.register(Potential)


class CDBRecordAdmin(admin.ModelAdmin):
    model = CDBRecord
    exclude = ('archive_filesize',)

admin.site.register(CDBRecord, CDBRecordAdmin)
