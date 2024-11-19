from django.db import models

# Create your models here.
from django.db import models
from django_resized import ResizedImageField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Image(models.Model):
    name = models.CharField(max_length=250,  unique=True)
    alternative = models.CharField(max_length=250)
    image = ResizedImageField(force_format="WEBP", quality=75, upload_to="images/",  unique=True)
    caption = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return self.name
        
    def get_absolute_api_url(self):
        return reverse("blog:api-v1:folder_name-detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['-uploaded_at']
        

class Video(models.Model):
    name = models.CharField(max_length=250,  unique=True)
    alternative = models.CharField(max_length=250)
    video = models.FileField(upload_to='videos/',  unique=True)
    caption = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_api_url(self):
        return reverse("blog:api-v1:folder_name-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-uploaded_at']
        
        
class URL(models.Model):
    name = models.CharField(max_length=250,  unique=True)
    alternative = models.CharField(max_length=250)
    url = models.URLField( unique=True)
    caption = models.TextField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  

    def get_tags(self):
        return ", ".join([t.name for t in self.tags.all()])
        
    class Meta:
        ordering = ['-added_at']
        

class Tag(models.Model):
    name = models.CharField(max_length=30,  unique=True)
    confirm = models.BooleanField(default=False,)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        

class TypeOfNews(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
      

class SourceOfNews(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
      

class MetaKword(models.Model):
    name = name = models.CharField(max_length=70, unique=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
      

