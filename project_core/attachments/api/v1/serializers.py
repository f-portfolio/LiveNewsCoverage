from attachments.models import Image, Video, URL, Tag, TypeOfNews, MetaKword
from rest_framework import serializers, permissions


class ImageSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'name', 'alternative', 'caption', 'image', 'uploaded_at', 'absolute_url']

    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs').get('pk') :
            rep.pop('absolute_url', None)
        # when call a serializer into another serializer should also pass the request
        return rep

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
class VideoSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'name', 'alternative', 'caption', 'video', 'uploaded_at', 'absolute_url']

    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs').get('pk') :
            rep.pop('absolute_url', None)
        # when call a serializer into another serializer should also pass the request
        return rep

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)


class URLSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = URL
        fields = ['id', 'name', 'alternative', 'caption', 'url', 'added_at', 'absolute_url']

    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs').get('pk') :
            rep.pop('absolute_url', None)
        # when call a serializer into another serializer should also pass the request
        return rep

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'confirm']

class TypeOfNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfNews
        fields = ['id', 'name']


class MetaKwordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfNews
        fields = ['id', 'name']
