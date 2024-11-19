from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'api-v1'

urlpatterns = [    
    path('image/',ImageModelViewSet.as_view({'get':'list', 'post':'create'}), name="image-list"),
    path('image/<int:pk>/',ImageModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="image-detail"),
    
    path('video/',VideoModelViewSet.as_view({'get':'list', 'post':'create'}), name="video-list"),
    path('video/<int:pk>/',VideoModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="video-detail"),
    
    path('url/',URLModelViewSet.as_view({'get':'list', 'post':'create'}), name="url-list"),
    path('url/<int:pk>/',URLModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="url-detail"),

    path('tag/',TagModelViewSet.as_view({'get':'list', 'post':'create'}), name="tag-list"),
    path('tag/<int:pk>/',TagModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="tag-detail"),
    path('tag/<str:tag_name>/', CheckIfTagIsConfirmedSView.as_view()),
    
    path('type_of_news/',TypeOfNewsModelViewSet.as_view({'get':'list', 'post':'create'}), name="type_of_news-list"),
    path('type_of_news/<int:pk>/',TypeOfNewsModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="type_of_news-detail"),
    
    path('meta_kword/',MetaKwordModelViewSet.as_view({'get':'list', 'post':'create'}), name="meta_kword-list"),
    path('meta_kword/<int:pk>/',MetaKwordModelViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="meta_kword-detail"),
]
