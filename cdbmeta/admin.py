from django.contrib import admin

from .models import (Attribution, LatticeParameters, Material,
                     DataColumn, CDBRecord)
from .models import CDBRecord

admin.site.register(Attribution)
admin.site.register(LatticeParameters)
admin.site.register(Material)
admin.site.register(DataColumn)


class CDBRecordAdmin(admin.ModelAdmin):
    model = CDBRecord

admin.site.register(CDBRecord, CDBRecordAdmin)
