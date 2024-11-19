# Register your models here.
from django.contrib import admin
from attachments.models import Image, Video, URL, Tag, TypeOfNews, MetaKword, SourceOfNews, TypeOfElection
from easy_select2.widgets import Select2, Select2Multiple


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    date_hierarchy = 'uploaded_at'
    empty_value_display = '-empty-'
    list_display = ('id', 'name', 'alternative', 'uploaded_at')
    list_filter = ('name', )
    search_fields = ['name', 'alternative', 'caption']
    list_display_links = ['id', 'name', ]
    

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    date_hierarchy = 'uploaded_at'
    empty_value_display = '-empty-'
    list_display = ('id', 'name', 'alternative', 'uploaded_at')
    list_filter = ('name', )
    search_fields = ['name','alternative', 'caption']
    list_display_links = ['id', 'name', ]

    
@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    date_hierarchy = 'added_at'
    empty_value_display = '-empty-'
    list_display = ('id', 'name', 'alternative', 'added_at')
    list_filter = ('name',)
    search_fields = ['name', 'alternative', 'caption']
    list_display_links = ['id', 'name', ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'confirm']
    list_display_links = ['id', 'name', ]
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser or not request.user.is_supervisor:
            return ['confirm']
        return []


@admin.register(TypeOfNews)
class TypeOfNewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]


@admin.register(MetaKword)
class MetaKwordAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]
 

@admin.register(SourceOfNews)
class SourceOfNewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]
 
 

