from django.contrib import admin

from .models import (Attribution, LatticeParameters, Material,
                     DataColumn, CDBRecord, Potential)
from .models import CDBRecord

admin.site.register(Attribution)
admin.site.register(LatticeParameters)
admin.site.register(Material)
admin.site.register(DataColumn)
admin.site.register(Potential)


class CDBRecordAdmin(admin.ModelAdmin):
    model = CDBRecord
    exclude = ('archive_filesize',)

admin.site.register(CDBRecord, CDBRecordAdmin)
