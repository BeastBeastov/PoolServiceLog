from django.contrib import admin

from blog.models import Post, Answer


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','author','time_create']
    list_display_links = ['id','title',]
    # search_fields = ['last_name','time_create']
    # list_editable = ['age',]
    # list_filter = ['status','gender','gto','polosa','children','orienteering']
    # ordering = ['last_name']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'time_create']
    list_display_links = ['id', ]


admin.site.register(Post, PostAdmin)
admin.site.register(Answer, AnswerAdmin)