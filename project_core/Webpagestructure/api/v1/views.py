from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import *
from Webpagestructure.models import *
from .permissions import *
from Webpagestructure.api.v1.paginations import CustomPageNumberPagination
from rest_framework import viewsets




class SiteHeaderModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly | IsSupervisor | IsSuperuser]
    serializer_class = SiteHeaderSerializer
    queryset = SiteHeader.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', ]
    search_fields = ['name', 'alternative_logo', ]
    ordering_fields = ['-created_date']
    pagination_class = CustomPageNumberPagination
    

class LinkSectionInFooterModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly | IsSupervisor | IsSuperuser]
    serializer_class = LinkSectionInFooterSerializer
    queryset = LinkSection.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['link',]
    search_fields = ['name', 'alternative_link', 'link' ]
    ordering_fields = ['-created_date']
    pagination_class = CustomPageNumberPagination
    

class SocialSectionInFooterModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly | IsSupervisor | IsSuperuser]
    serializer_class = SocialSectionInFooterSerializer
    queryset = SocialSection.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['link',]
    search_fields = ['name', 'alternative_link', 'link', 'alternative_logo']
    ordering_fields = ['-created_date']
    pagination_class = CustomPageNumberPagination
    

class SiteFooterModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly | IsSupervisor | IsSuperuser]
    serializer_class = SiteFooterSerializer
    queryset = SiteFooter.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['links_section', 'social_section', 'link_of_right_of_ownership_site',]
    search_fields = ['legal_sentence_of_right_of_ownership', 'link_of_right_of_ownership_site']
    ordering_fields = ['-created_date']
    pagination_class = CustomPageNumberPagination
    

class SiteThemeModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly | IsSupervisor | IsSuperuser]
    serializer_class = SiteThemeSerializer
    queryset = SiteTheme.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['theme_name', 'black', 'white', 'gray', 'primaryColor', 'secondaryColor', 'gradientFirstColor', 'gradientSecondColor', 'type_theme']
    search_fields = ['theme_name', 'black', 'white', 'gray', 'primaryColor', 'secondaryColor', 'gradientFirstColor', 'gradientSecondColor', 'type_theme']
    ordering_fields = ['theme_name']
    pagination_class = CustomPageNumberPagination
    

class SiteStructureModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGetOnly | IsSupervisor | IsSuperuser]
    #permission_classes = [IsOwnerOrReadOnly, IsGetOnly | IsAdminUser]
    serializer_class = SiteStructureSerializer
    queryset = SiteStructure.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['site_name', 'header', 'fooer', 'dark_theme', 'light_theme',]
    search_fields = ['site_name', 'header__name', 'dark_theme__name', 'light_theme__name',]
    ordering_fields = ['-created_date']
    pagination_class = CustomPageNumberPagination
    

