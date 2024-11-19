import calendar
import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from django_summernote.admin import SummernoteModelAdmin
from blog.models import Post, FolderName, CrawlSearchWord
from blog.forms import MyModelAdminForm
from easy_select2.widgets import Select2, Select2Multiple


class DateRangeFilter(admin.SimpleListFilter):
    title = 'Date Range'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('this_week', 'This Week'),
            ('this_month', 'This Month'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(created_date__date=datetime.date.today())
        elif self.value() == 'this_week':
            start_date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
            end_date = start_date + datetime.timedelta(days=6)
            return queryset.filter(created_date__date__range=[start_date, end_date])
        elif self.value() == 'this_month':
            start_date = datetime.date.today().replace(day=1)
            end_date = start_date + datetime.timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1] - 1)
            return queryset.filter(created_date__date__range=[start_date, end_date])


class DateRangeFilter(admin.SimpleListFilter):
    title = 'Date Range'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('this_week', 'This Week'),
            ('this_month', 'This Month'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(created_date__date=datetime.date.today())
        elif self.value() == 'this_week':
            start_date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
            end_date = start_date + datetime.timedelta(days=6)
            return queryset.filter(created_date__date__range=[start_date, end_date])
        elif self.value() == 'this_month':
            start_date = datetime.date.today().replace(day=1)
            end_date = start_date + datetime.timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1] - 1)
            return queryset.filter(created_date__date__range=[start_date, end_date])
        

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
# class PostAdmin(admin.ModelAdmin):
    actions = ['export_selected_to_csv']
    list_per_page = 50
    raw_id_fields = ('image', 'video', 'url')
    list_display_links = ['id', "publisher", "folder_name", 'title', 'author']
    form = MyModelAdminForm
    date_hierarchy = 'published_date'
    empty_value_display = '-empty-'
    list_display = ('id', 'trash', 'confirm_to_post', 'is_pined', 'status', 'title', 'publisher', 'author', 
                    'folder_name', 'supervisor_to_confirm', 'supervisor_to_pined', 'type_of_news', 
                    'source_website', 'word_count', 'counted_views', 'created_date', 
                    'published_date')
    
    list_filter = ('publisher', 'author', 'folder_name', 'tags', 'status', 'confirm_to_post', 
                   'is_pined', 'supervisor_to_confirm', 'supervisor_to_pined', 'type_of_news', 
                   'source_website', 'trash', DateRangeFilter)
    
    search_fields = ['folder_name__name', 'author__user__username', 'publisher__user__username', 
                     'title', 'h1', 'tags__name', 'slog', 'content', 'snippet', 
                     'type_of_news__name', 'source_website__name', 'media_description',]
    summernote_fields = ['content']
    # readonly_fields = ('status', 'slog', 'article_reference')
    ordering = ('-created_date', )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'folder_name' or db_field.name=="publisher"\
            or db_field.name=="author" or db_field.name=="type_of_news" or \
            db_field.name=="source_website" or db_field.name=="supervisor_to_confirm"\
            or db_field.name=="supervisor_to_pined":
            kwargs['widget'] = Select2()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags' or db_field.name == 'meta_kword':
            kwargs['widget'] = Select2Multiple()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
     
    def export_selected_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="shifts.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(['id', 'folder_name', 'publisher', 'author', 'ro_titer', 'h1', 'slog', 
                         'title', 'snippet', 'meta_description', 'content', 'image', 'image_url', 
                         'video', 'video_url', 'url', 'embed_code', 'media_description', 
                         'type_of_news', 'source_website', 'meta_kword', 'tags', 'counted_views', 
                         'status', 'confirm_to_post', 'supervisor_to_confirm', 'is_pined', 
                         'supervisor_to_pined', 'trash', 
                         'created_date', 'updated_date', 'published_date', ])
        for shift in queryset:
            writer.writerow([shift.id, shift.publisher, 
                            #  shift.start_time.strftime('%H:%M'), shift.end_time.strftime('%H:%M'),
                             shift.folder_name, 
                            #  shift.site_id, shift.user_id, shift.status
                            ])

        return response

    export_selected_to_csv.short_description = "Export selected to CSV"
    
    def get_readonly_fields(self, request, obj=None):
        # If the user is not a supervisor, make the confirm_to_post field read-only
        if not request.user.is_supervisor:
            return self.readonly_fields + ('confirm_to_post', 'supervisor_to_confirm', 'is_pined',
                                            'supervisor_to_pined', 'counted_views')
        return self.readonly_fields

    #def get_form(self, request, obj=None, **kwargs):
    #    form = super().get_form(request, obj, **kwargs)
    #    if request.user.is_authenticated:
    #        form.base_fields['author'].queryset = form.base_fields['author'].queryset.filter(user=request.user)
    #    return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # If the user is not a moderator, filter the queryset to show only their own posts
        if not request.user.is_supervisor:
            queryset = queryset.filter(publisher__user=request.user)
        
        return queryset
    
    @admin.display(description="word_count")
    def word_count(self, obj):
        return len(obj.content.split(' '))

@admin.register(FolderName)
class FolderNameAdmin(admin.ModelAdmin):
    list_per_page = 15
    raw_id_fields = ('heder_img', 'folder_img')
    list_display_links = ['id', "name"]
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('id', 'trash', 'is_pined', 'is_active', 'name', 
                    'supervisor_to_pined', 'counted_views', 'heder_img', 
                    'folder_img',  'created_date', 'updated_date')
    list_filter = ('name', 'tags', 'is_active', 'trash',)
    search_fields = ['name', 'h1', 'header', 'tags__name']
    readonly_fields = ('slog',)
    ordering = ('-created_date', )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'supervisor_to_pined':
            kwargs['widget'] = Select2()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags' or db_field.name == 'meta_kword':
            kwargs['widget'] = Select2Multiple()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        # If the user is not a supervisor, make the confirm_to_post field read-only
        if not request.user.is_supervisor:
            return self.readonly_fields + ('is_pined', 'supervisor_to_pined')
        return self.readonly_fields


@admin.register(CrawlSearchWord)
class CrawlSearchWordAdmin(admin.ModelAdmin):
    list_per_page = 8
    raw_id_fields = ('folder_name', )
    list_display_links = ['id', 'folder_name', 'word1', 'word2', 'word3', 'word4', 'word5', ]
    empty_value_display = '-empty-'
    list_display = ('id', 'folder_name', 'word1', 'word2', 'word3', 'word4', 'word5', )
    
    list_filter = ('folder_name', 'word1', 'word2', 'word3', 'word4', 'word5', )
    
    search_fields = ['folder_name__name', 'word1', 'word2', 'word3', 'word4', 'word5',]
    ordering = ('id', )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'folder_name' :
            kwargs['widget'] = Select2()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
