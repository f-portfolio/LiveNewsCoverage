from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'api-v1'

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns = [
    path('post/',PostModelViewSet.as_view({'get':'list', 'post':'create'}), name="post-list"),
    path('post/<int:pk>/',PostDetail.as_view(), name="post-detail"),
    path('posts/<strtart_date>/<str:end_date>/', PostsInRangeView.as_view(), name='posts_in_range'),

    path('folder_name/',FolderNameModelViewSet.as_view({'get':'list', 'post':'create'}), name="folder_name-list"),
    path('folder_name/<int:pk>/',FolderNameDetail.as_view(), name="folder_name-detail"),
    path('categories/<int:folder_name_id>/', PostListByFolderName.as_view(), name='post-list-by-folder_name'),

    path('crawl_web/',NewsViewset.as_view({'get':'list'}),name="crawl_web"),
    
    path('crawl-search-words/', CrawlSearchWordListCreateView.as_view(), name='crawl_search_words'),
    path('crawl-search-words/<int:pk>/', CrawlSearchWordDetail.as_view(), name='crawl_search_word_detail'),

    path('post_status/',PostStatusModelViewSet.as_view({'get':'list', 'post':'create'}), name="post-status-list"),
]


