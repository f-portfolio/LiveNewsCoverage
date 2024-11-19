from Webpagestructure.models import *
from accounts.models import Profile
from rest_framework import serializers, permissions
from rest_framework.exceptions import ValidationError

#from django.utils import timezone


class SiteHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteHeader
        fields = ['id', 'name', 'logo', 'alternative_logo',] # 'created_date', 'updated_date']
       
    def validate_name(self, value):
        if SiteHeader.objects.filter(name=value).exists():
            raise ValidationError("This name is already used, please choose another name.")
        return value



class LinkSectionInFooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkSection
        fields = ['id', 'name', 'link', 'alternative_link', ]
        


class SocialSectionInFooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialSection
        fields = ['id', 'name', 'link', 'alternative_link', 'logo', 'alternative_logo',]
        


class SiteFooterSerializer(serializers.ModelSerializer): 
    class Meta:
        model = SiteFooter
        fields = ['id', 'links_section', 'social_section', 'legal_sentence_of_right_of_ownership', 
                  'link_of_right_of_ownership_site', ]
    
    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        rep['links_section'] = LinkSectionInFooterSerializer(instance.links_section.all(), context={'request':request}, many=True).data
        rep['social_section'] = SocialSectionInFooterSerializer(instance.social_section.all(), context={'request':request}, many=True).data
        return rep
    

class SiteThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteTheme
        fields = ['id', 'theme_name', 'black', 'white', 'gray', 'primaryColor', 
                  'secondaryColor', 'gradientFirstColor', 'gradientSecondColor', 'type_theme']
       


class SiteStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStructure
        fields = ['id', 'site_name', 'header', 'fooer', 'dark_theme', 'light_theme', ]
    
    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        rep['header'] = SiteHeaderSerializer(instance.header, context={'request':request}).data
        rep['fooer'] = SiteFooterSerializer(instance.fooer, context={'request':request}).data
        rep['dark_theme'] = SiteThemeSerializer(instance.dark_theme, context={'request':request}).data
        rep['light_theme'] = SiteThemeSerializer(instance.light_theme, context={'request':request}).data
        return rep
    

