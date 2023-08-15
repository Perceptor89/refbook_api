from django.contrib import admin
from refbook.models import Refbook


admin.site.site_header = 'Справочники'
admin.site.index_title = 'Управление справочниками'


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'current_version']

    @admin.display(description='текущая версия', empty_value='-empty-')
    def current_version(self, obj):
        return obj.versions.first()
