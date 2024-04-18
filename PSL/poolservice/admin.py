from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class PoolServiceAdmin(admin.ModelAdmin):
    list_display = ['id','title','pool','PH','RX','CL','T','time_create','is_published']
    list_display_links = ['id','title','time_create']
    search_fields = ['title','pool']
    list_editable = ['is_published']
    list_filter = ['is_published','title','pool','time_create']


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ['id','title','volume','phone','get_html_photo']
    list_display_links = ['id','title']
    search_fields = ['title']
    prepopulated_fields = {'slug':('title',)}

    def get_html_photo(self,object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "МиниФото"


admin.site.register(Reagent)
admin.site.register(ReagentName)
admin.site.register(PoolService, PoolServiceAdmin)