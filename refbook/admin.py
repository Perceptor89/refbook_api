from typing import Any
from django.contrib import admin
from refbook.models import Refbook, RefbookVersion, RefbookElement
from django.contrib.auth.models import User, Group


admin.site.site_header = 'Справочники'
admin.site.index_title = 'Управление справочниками'
admin.site.unregister(User)
admin.site.unregister(Group)


class VersionInline(admin.TabularInline):
    model = RefbookVersion
    extra = 1

@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'cur_ver', 'cur_ver_from']
    list_display_links = ['name']
    empty_value_display = '-empty-'
    inlines = [
        VersionInline,
    ]

    @admin.display(description='текущая версия')
    def cur_ver(self, obj):
        cur_ver = obj.current_version()
        if cur_ver:
            return cur_ver.version

    @admin.display(description='действует с')
    def cur_ver_from(self, obj):
        cur_ver = obj.current_version()
        if cur_ver:
            return cur_ver.active_from 


class ElementInline(admin.StackedInline):
    model = RefbookElement
    extra = 1


@admin.register(RefbookVersion)
class RefbookVersionAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'version', 'active_from', 'refbook_code', 'refbook_name']
    list_display_links = ['version']
    inlines = [
        ElementInline,
    ]

    @admin.display(description='Код справочника')
    def refbook_code(self, obj):
        return obj.refbook.code

    @admin.display(description='Имя справочника')
    def refbook_name(self, obj):
        return obj.refbook.name


@admin.register(RefbookElement)
class RefbookElementAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'refbook_version', 'code', 'value']
