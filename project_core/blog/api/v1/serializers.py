from blog.models import Post, FolderName, CrawlSearchWord
from accounts.models import Profile
from attachments.models import Image, Video, URL, TypeOfNews, SourceOfNews, MetaKword, Tag
from rest_framework import serializers, permissions
from django.utils import timezone
from datetime import timedelta

class PostSerializer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')
    word_count = serializers.SerializerMethodField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if ('request' in self.context 
            and self.context['request'].user.is_authenticated 
            and self.context['request'].user.is_verified
            and self.context['request'].user.is_staff):
            self.Meta.read_only_fields = ['publisher', 'counted_views', 'word_count', 'trash', 
                                          'article_reference','status', 'slog', 'confirm_to_post',
                                            'supervisor_to_confirm', 'is_pined', 'supervisor_to_pined',]

        elif ('request' in self.context 
            and self.context['request'].user.is_authenticated 
            and self.context['request'].user.is_verified
            and self.context['request'].user.is_supervisor):
            self.Meta.read_only_fields = ['publisher', 'counted_views', 'word_count', 'slog',
                                          'article_reference',]

        else:
            self.Meta.read_only_fields = ['id', 'folder_name', 'author', 'publisher', 'title', 
                                          'h1', 'meta_description', 'meta_kword', 'ro_titer',
                                          'content', 'snippet', 'image', 'video', 'url', 
                                          'embed_code' , 'slog', 'media_description', 'type_of_news', 
                                          'tags', 'counted_views', 'status', 'confirm_to_post', 
                                          'supervisor_to_confirm', 'source_website', 'word_count',
                                          'trash', 'article_reference', 'created_date', 'updated_date', 
                                          'published_date', 'relative_url', 'absolute_url',
                                          'is_pined', 'supervisor_to_pined',]

    class Meta:
        model = Post
        fields = ['id', 'folder_name', 'author', 'publisher', 'title', 'h1', 'meta_description', 
                  'meta_kword', 'ro_titer', 'content', 'snippet', 'image', 'video', 'url', 
                  'image_url', 'video_url', 'embed_code' , 'slog', 'media_description', 
                  'type_of_news', 'tags', 'counted_views', 'status', 'confirm_to_post', 
                  'supervisor_to_confirm', 'is_pined', 'supervisor_to_pined','source_website', 
                  'article_reference', 'word_count', 'trash', 'created_date', 'updated_date', 
                  'published_date', 'relative_url', 'absolute_url']
        
        
    # same name as line 15  
    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
  
    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs').get('pk') :
            rep.pop('snippet', None)
            rep.pop('relative_url', None)
            rep.pop('absolute_url', None)
        else:
            # rep.pop('content', None)
            pass
        # when call a serializer into another serializer should also pass the request
        rep['folder_name'] = CategorySerializer(instance.folder_name, context={'request':request}).data
        rep['author'] = ProfileSerializer(instance.author, context={'request':request}).data
        rep['publisher'] = ProfileSerializer(instance.publisher, context={'request':request}).data
        rep['image'] = ImageSerializer(instance.image, context={'request':request}).data
        rep['video'] = videoSerializer(instance.video, context={'request':request}).data
        rep['url'] = URLSerializer(instance.url, context={'request':request}).data
        rep['type_of_news'] = TypeOfNewsSerializer(instance.type_of_news, context={'request':request}).data
        rep['source_website'] = SourceOfNewsSerializer(instance.source_website, context={'request':request}).data
        rep['meta_kword'] = MetaKwordSerializer(instance.meta_kword.all(), context={'request':request}, many=True).data
        rep['tags'] = TagSerializer(instance.tags.all(), context={'request':request}, many=True).data
        return rep
    
    def get_word_count(self, obj):
        return len(obj.content.split(' '))

    def create(self,validated_data):
        #validated_data['publisher'] = Profile.objects.get(user__id=self.context.get('request').user.id)
       
        request = self.context.get('request')
        user = request.user

        validated_data['publisher'] = Profile.objects.get(user__id=user.id)
        if ('request' in self.context 
            and self.context['request'].user.is_authenticated 
            and self.context['request'].user.is_verified
            and self.context['request'].user.is_supervisor):
            validated_data['confirm_to_post'] = True
            validated_data['supervisor_to_confirm'] = Profile.objects.get(user__id=user.id)
        
        if validated_data['published_date'] <= timezone.now():
            validated_data['status'] = True
        else:
            validated_data['status'] = False

        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        if 'published_date' not in validated_data:
            validated_data['published_date'] = instance.published_date
        
        if validated_data['published_date'] <= timezone.now():
            validated_data['status'] = True
        else:
            validated_data['status'] = False
   
        return super().update(instance, validated_data)

class PostsFilterByDateSerializer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    word_count = serializers.SerializerMethodField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if ('request' in self.context 
            and self.context['request'].user.is_authenticated 
            and self.context['request'].user.is_verified
            and self.context['request'].user.is_staff):
            self.Meta.read_only_fields = ['publisher', 'counted_views', 'word_count', 'trash',
                                          'status', 'slog', 'confirm_to_post', 'supervisor_to_confirm']

        elif ('request' in self.context 
            and self.context['request'].user.is_authenticated 
            and self.context['request'].user.is_verified
            and self.context['request'].user.is_supervisor):
            self.Meta.read_only_fields = ['publisher', 'counted_views', 'word_count', 'slog',]

        else:
            self.Meta.read_only_fields = ['id', 'folder_name', 'author', 'publisher', 'title', 'h1', 'meta_description', 'meta_kword', 'ro_titer',
                  'content', 'snippet', 'image', 'video', 'url', 'embed_code' , 'slog',
                  'media_description', 'type_of_news', 'tags', 'counted_views', 'status', 'confirm_to_post', 
                  'supervisor_to_confirm', 'source_website', 'word_count', 'trash',
                  'created_date', 'updated_date', 'published_date', 'relative_url']

    class Meta:
        model = Post
        fields = ['id', 'folder_name', 'author', 'publisher', 'title', 'h1', 'meta_description', 'meta_kword', 'ro_titer',
                  'content', 'snippet', 'image', 'video', 'url', 'embed_code' , 'slog',
                  'media_description', 'type_of_news', 'tags', 'counted_views', 'status', 'confirm_to_post', 
                  'supervisor_to_confirm', 'source_website', 'word_count', 'trash',
                  'created_date', 'updated_date', 'published_date', 'relative_url']

    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
  
    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        rep['folder_name'] = CategorySerializer(instance.folder_name, context={'request':request}).data
        rep['author'] = ProfileSerializer(instance.author, context={'request':request}).data
        rep['publisher'] = ProfileSerializer(instance.publisher, context={'request':request}).data
        rep['image'] = ImageSerializer(instance.image, context={'request':request}).data
        rep['video'] = videoSerializer(instance.video, context={'request':request}).data
        rep['url'] = URLSerializer(instance.url, context={'request':request}).data
        rep['type_of_news'] = TypeOfNewsSerializer(instance.type_of_news, context={'request':request}).data
        rep['source_website'] = SourceOfNewsSerializer(instance.source_website, context={'request':request}).data
        rep['meta_kword'] = MetaKwordSerializer(instance.meta_kword.all(), context={'request':request}, many=True).data
        rep['tags'] = TagSerializer(instance.tags.all(), context={'request':request}, many=True).data
        return rep
    
    def get_word_count(self, obj):
        return len(obj.content.split(' '))

    def create(self,validated_data):       
        request = self.context.get('request')
        user = request.user

        validated_data['publisher'] = Profile.objects.get(user__id=user.id)
        if ('request' in self.context 
            and self.context['request'].user.is_authenticated 
            and self.context['request'].user.is_verified
            and self.context['request'].user.is_supervisor):
            validated_data['confirm_to_post'] = True
            validated_data['supervisor_to_confirm'] = Profile.objects.get(user__id=user.id)

        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        if 'published_date' not in validated_data:
            validated_data['published_date'] = instance.published_date
        return super().update(instance, validated_data)


class PostSerializer_(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['id', 'folder_name', 'author', 'publisher', 'title', 'meta_kword',
                  'content', 'snippet','image_url', 'url', 
                  'media_description', 'type_of_news', 'tags',
                  'supervisor_to_confirm', 'source_website',
                  'published_date']


class FolderNameSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if ('request' in self.context 
            and self.context['request'].user.is_authenticated 
            and self.context['request'].user.is_verified
            and self.context['request'].user.is_supervisor):
            self.Meta.read_only_fields = ['supervisor_to_pined', 'slog',]
        else:
            self.Meta.read_only_fields = ['id', 'name', 'h1', 'header', 'header', 'meta_description', 'meta_kword','is_pined', 'supervisor_to_pined', 'trash', 'slog',
                  'abstract', 'tags', 'is_active', 'heder_img', 'folder_img', 'counted_views', 'updated_date', 'created_date', 'absolute_url']
    
    class Meta:
        model = FolderName
        fields = ['id', 'name', 'h1', 'header', 'meta_description', 'meta_kword','is_pined', 'supervisor_to_pined', 'trash', 'slog',
                  'abstract', 'tags', 'is_active', 'heder_img', 'folder_img', 'counted_views', 'updated_date', 'created_date', 'absolute_url']

    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs').get('pk') :
            rep.pop('absolute_url', None)
        # when call a serializer into another serializer should also pass the request
        # rep['tags'] = TagSerializer(instance.tags, context={'request':request}).data
        return rep

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    
    def create(self,validated_data):
        #validated_data['publisher'] = Profile.objects.get(user__id=self.context.get('request').user.id)
       
        request = self.context.get('request')
        user = request.user
    
        #validated_data['publisher'] = Profile.objects.get(user__id=user.id)
        if ('request' in self.context 
            and self.context['request'].user.is_authenticated 
            and self.context['request'].user.is_verified
            and self.context['request'].user.is_supervisor
            and self.is_pined):
            validated_data['is_pined'] = True
            validated_data['supervisor_to_pined'] = Profile.objects.get(user__id=user.id)
    
        return super().create(validated_data)
    

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name']



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FolderName
        fields = ['id', 'name']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name',]


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"


class videoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = "__all__"


class URLSerializer(serializers.ModelSerializer):

    class Meta:
        model = URL
        fields = "__all__"


class TypeOfNewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOfNews
        fields = ['id', 'name']


class SourceOfNewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourceOfNews
        fields = ['id', 'name']



class MetaKwordSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetaKword
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class CrawlSearchWordSerializer(serializers.ModelSerializer):
    folder_name = serializers.PrimaryKeyRelatedField(queryset=FolderName.objects.all())
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')


    class Meta:
        model = CrawlSearchWord
        fields = ['id', 'folder_name', 'word1', 'word2', 'word3', 'word4', 'word5', 'absolute_url']

    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk') :
            rep.pop('absolute_url', None)
        rep['folder_name'] = TagSerializer(instance.folder_name, context={'request':request}).data
        return rep


