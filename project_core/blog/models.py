from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from attachments.models import Image, Video, URL, Tag, MetaKword, TypeOfNews, SourceOfNews
from django.core.exceptions import ValidationError
import re
from datetime import timedelta
from django.utils import timezone

class Post(models.Model):
    folder_name = models.ForeignKey('blog.FolderName', on_delete=models.CASCADE)
    publisher = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='posts_publisher')
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='posts')
    
    ro_titer = models.CharField( max_length=70, null=True, blank=True)
    h1 = models.CharField(max_length=70, unique=True, ) 
    slog = models.CharField(max_length=25, null=True, blank=True,)
    title = models.CharField( max_length=70, null=True, blank=True,) 
    snippet = models.TextField(max_length=150)
    meta_description = models.CharField(max_length=150, null=True, blank=True)
    content = models.TextField()
    
    image = models.ForeignKey("attachments.Image", on_delete=models.SET_NULL, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True,)
    video = models.ForeignKey("attachments.Video", on_delete=models.SET_NULL, null=True, blank=True)
    video_url = models.URLField( null=True, blank=True,)
    url = models.ForeignKey("attachments.URL", on_delete=models.SET_NULL, null=True, blank=True)
    embed_code = models.TextField( null=True, blank=True, )
    media_description = models.CharField( max_length=255, null=True, blank=True)
    
    type_of_news = models.ForeignKey("attachments.TypeOfNews", on_delete=models.SET_NULL, null=True, blank=True)
    source_website = models.ForeignKey("attachments.SourceOfNews", on_delete=models.SET_NULL, null=True, blank=True)
    
    meta_kword = models.ManyToManyField("attachments.MetaKword",)
    tags = models.ManyToManyField("attachments.Tag", limit_choices_to={'confirm': True}, related_name='posts_tag')
    
    counted_views = models.IntegerField(null=True, default=0)
    status = models.BooleanField(default=False,)
    
    confirm_to_post = models.BooleanField(default=False,)
    supervisor_to_confirm = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='confirmed_posts')

    is_pined = models.BooleanField(default=False,)
    supervisor_to_pined = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='pined_posts_blog')
    
    trash = models.BooleanField( default=False,)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True,)
    
    article_reference = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})
    
    def clean(self):
        if (self.image or self.video or self.url) and not self.media_description:
            raise ValidationError({'media_description': 'The media_description field must be filled.'})
    
    def save(self, *args, **kwargs):
        
        if re.findall(r' style="(.*?)"', self.content):
            pattern = r' style="(.*?)"'
            replacement = ''
            self.content = re.sub(pattern, replacement, self.content)
        
        if re.findall(r''' style=".*
(.*?)"''', self.content):
            pattern = r''' style=".*
(.*?)"'''
            replacement = ''
            self.content = re.sub(pattern, replacement, self.content)
        
        if self.published_date <= self.created_date:
            self.status = True

        if self.published_date <= timezone.now():
            self.status = True

        if self.supervisor_to_confirm and self.supervisor_to_confirm.user.is_supervisor \
            and self.confirm_to_post:
            self.supervisor_to_confirm = self.supervisor_to_confirm
        else: 
            self.supervisor_to_confirm = None
            self.confirm_to_post = False
        
        if self.confirm_to_post == False:
            self.supervisor_to_confirm = None
            self.confirm_to_post = False
        
        if self.supervisor_to_pined and self.supervisor_to_pined.user.is_supervisor \
            and self.is_pined:
            self.supervisor_to_pined = self.supervisor_to_pined
        else: 
            self.supervisor_to_pined = None
            self.is_pined = False
        
        if self.is_pined == False:
            self.supervisor_to_pined = None
            self.is_pined = False
        
        if not self.h1:  # Check if h1 is not filled
            self.h1 = self.title  # Copy title to h1
        
        if not self.title: 
            self.title = self.h1  

        if not self.meta_description:
            self.meta_description = self.snippet    
        
        super().save(*args, **kwargs)
        
    def get_tags(self):
        return ", ".join([t.name for t in self.tags.all()])
    
    def get_meta_kword(self):
        return ", ".join([t.name for t in self.tags.all()])
    
    class Meta:
        ordering = ['-published_date']
       

class FolderName(models.Model):
    heder_img = models.ForeignKey("attachments.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name='heder_img')
    folder_img = models.ForeignKey("attachments.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name='folder_img')
    
    h1 = models.CharField(max_length=70,  unique=True,) 
    header = models.CharField(max_length=20, null=True, blank=True, default= 'Live News')
    slog = models.CharField(max_length=25, null=True, blank=True,)
    name = models.CharField(max_length=70, null=True, blank=True,) 
    abstract = models.TextField( max_length=150,)
    meta_description = models.CharField( max_length=150, null=True, blank=True,)
    meta_kword = models.ManyToManyField(MetaKword, null=True, blank=True,)
    
    tags = models.ManyToManyField("attachments.Tag", limit_choices_to={'confirm': True}, related_name='folder_name_tag')
    is_active = models.BooleanField(default=False)
    counted_views = models.IntegerField(null=True, default=0)
    
    is_pined = models.BooleanField( default=False,)
    supervisor_to_pined = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, null=True, related_name='pined_foldername')

    trash = models.BooleanField( default=False,)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
        
    def get_absolute_api_url(self):
        return reverse("blog:api-v1:folder_name-detail", kwargs={"pk": self.pk})

    def get_tags(self):
        return ", ".join([t.name for t in self.tags.all()])

    def get_meta_kword(self):
        return ", ".join([t.name for t in self.tags.all()])

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):

        if self.supervisor_to_pined and self.supervisor_to_pined.user.is_supervisor and self.is_pined:
            self.supervisor_to_pined = self.supervisor_to_pined
        else: 
            self.supervisor_to_pined = None
            self.is_pined = False
        if self.is_pined == False:
            self.supervisor_to_pined = None
            self.is_pined = False

        if not self.name: 
            self.name = self.h1  

        if not self.meta_description:
            self.meta_description = self.abstract    
        
        super().save(*args, **kwargs)
     
    class Meta:
        ordering = ['-created_date']
        

class CrawlSearchWord(models.Model):
    folder_name = models.ForeignKey('blog.FolderName', on_delete=models.CASCADE, unique=True,)

    word1 = models.CharField(max_length=50,)
    word2 = models.CharField(max_length=50, null=True, blank=True)
    word3 = models.CharField(max_length=50, null=True, blank=True)
    word4 = models.CharField(max_length=50, null=True, blank=True)
    word5 = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.word1 
    
    class Meta:
        unique_together = ('word1', 'folder_name')
