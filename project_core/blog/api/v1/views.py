from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets, generics
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.decorators import permission_required
from .serializers import FolderNameSerializer, PostSerializer, TagSerializer, PostSerializer_, PostsFilterByDateSerializer, CrawlSearchWordSerializer
from blog.models import Post, FolderName, CrawlSearchWord
from .permissions import IsOwnerOrReadOnly, IsGetOnly#,  IsSupervisor,
import re 
from .paginations import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
import psycopg2

from selenium import webdriver
from ...models import Post
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime

from jdatetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .crawl_web import CrawlViewset
from .crawl_web import *
from .crawl_web import connection_to_database
import logging
from datetime import timedelta


logger = logging.getLogger(__name__)

class PostModelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] #IsAdminUser
    permission_classes = [IsOwnerOrReadOnly, IsGetOnly | IsAdminUser]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['folder_name', 'publisher', 'author', 'tags', 'status', 
                        'confirm_to_post', 'supervisor_to_confirm', 'is_pined', 
                        'is_pined', 'trash', 'supervisor_to_pined', 'supervisor_to_pined',
                        'type_of_news', 'source_website',]
    search_fields = ['folder_name__name', 'author__user__username', 'publisher__user__username', 
                     'title', 'h1', 'tags__name', 'content', 'type_of_news__name', 'media_description',]
    
    ordering_fields = ['-published_date']
    pagination_class = StandardPagination
    ##pagination_class = DefaultPagination
    

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self):
        # Increment the views_count when a user loads the post
        obj = super().get_object()
        obj.counted_views += 1
        obj.save()
        return obj


class FolderNameModelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, IsSupervisor]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsGetOnly | IsAdminUser]
    serializer_class = FolderNameSerializer
    queryset = FolderName.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'tags', 'trash',]
    search_fields = ['name', 'h1', 'header', 'tags__name']
    ordering = ['-created_date', ]
    pagination_class = StandardPagination
    

class FolderNameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FolderName.objects.all()
    serializer_class = FolderNameSerializer

    def get_object(self):
        # Increment the views_count when a user loads the post
        obj = super().get_object()
        obj.counted_views += 1
        obj.save()
        return obj
    

class PostListByFolderName(generics.ListAPIView):
    permission_classes = [IsOwnerOrReadOnly, IsGetOnly | IsAdminUser]
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['folder_name', 'publisher', 'author', 'tags', 'status', 
                        'confirm_to_post', 'supervisor_to_confirm', 'is_pined', 
                        'is_pined', 'trash', 'supervisor_to_pined', 'supervisor_to_pined',
                        'type_of_news', 'source_website',]
    search_fields = ['folder_name__name', 'author__user__username', 'publisher__user__username', 
                     'title', 'h1', 'tags__name', 'content', 'type_of_news__name', 'media_description',]
    pagination_class = StandardPagination

    def get_queryset(self):
        folder_name_id = self.kwargs['folder_name_id']
        logger.info(f"Retrieving posts for folder_name_id: {folder_name_id}")

        queryset = Post.objects.filter(status=False)
        for post in queryset:
            if post.published_date <= timezone.now():
                post.status = True
                post.save()

        return Post.objects.filter(folder_name=folder_name_id, confirm_to_post=True, status=True, trash=False)



class PostsInRangeView(APIView):
    def get(self, request, start_date, end_date):
        conn = connection_to_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM blog_post WHERE created_date > %s AND 
                           created_date < %s''', [start_date, end_date])
        
        post_range = cursor.fetchall()
        print(post_range)
        conn.close()
        posts = Post.objects.filter(created_date__range=[start_date, end_date])
        serialized_posts = PostsFilterByDateSerializer(posts, many=True)
        return Response({'post_count': len(serialized_posts.data), 'posts': serialized_posts.data})
    


class NewsViewset(viewsets.ViewSet):
    permission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer_
    queryset = Post.objects.all()
    # Definition of an instance of the web crawler page class
    def __init__(self):
        self.instance_of_crawlweb = CrawlViewset()
    
  
    def list(self, request):
        # Search for the desired text
        conn = connection_to_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM blog_foldername WHERE is_active = %s''',[True] )
        result = cursor.fetchall()
        conn.close()
            
        for r in result:
            # folder_name=r[3]
            folder_name_id=r[0]
            # print(folder_name_id,folder_name)
            conn = connection_to_database()
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM blog_crawlsearchword WHERE folder_name_id = %s''',[folder_name_id])
            searchname = cursor.fetchall()
            conn.close()
            for name in searchname:
                for n in name:
                        if (n is not None)  :
                            try:
                                if int(n):
                                    pass
                            except ValueError:
                                chrome_options = Options()
                                chrome_options.add_argument("--headless")
                                driver = webdriver.Chrome(options=chrome_options)
                                # driver = webdriver.Chrome()
                                driver.get("your url page")
                                wait = WebDriverWait(driver, 5)

                                searchpageone = wait.until(EC.presence_of_element_located(
                                    (By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div/div/div/form/div/div/input")))
                                searchpageone.send_keys(n)
                                searchpageone.send_keys(Keys.ENTER)
                                for i in range(1,10,1):
                                        # Check the search results to get the news base
                                        path = '//*[@id="search_results_wrapper"]/div['+str(i)+']/div[1]/div[2]/div[2]/span/a'
                                        urlsite = wait.until(EC.presence_of_element_located(
                                            (By.XPATH, path))).get_attribute('href')
                                        print(urlsite)

                                        # The names of the news you want -> xxx, yyy, ccc,
                                        if urlsite.endswith("xxx"):
                                            self.instance_of_crawlweb.xxx_crawl(i, wait,folder_name_id)
                                        
                                        elif urlsite.endswith("yyy"):
                                            self.instance_of_crawlweb.yyy_crawl(i, wait,folder_name_id)

                                        elif urlsite.endswith("ccc"):
                                            self.instance_of_crawlweb.ccc_crawl(i, wait, folder_name_id)
                
                                        else:
                                            print('not found')
                                driver.close()
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class CrawlSearchWordListCreateView(generics.ListCreateAPIView):
    queryset = CrawlSearchWord.objects.all()
    serializer_class = CrawlSearchWordSerializer
    permission_classes = [IsGetOnly | IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['folder_name', 'word1', 'word2', 'word3', 'word4', 'word5']
    search_fields = ['folder_name', 'word1', 'word2', 'word3', 'word4', 'word5']
    ordering = ['folder_name', ]


class CrawlSearchWordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrawlSearchWord.objects.all()
    serializer_class = CrawlSearchWordSerializer


class PostStatusModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsGetOnly | IsAdminUser]
    serializer_class = PostSerializer

    queryset = Post.objects.filter(status=False)
    for post in queryset:
        now = timezone.now()
        new_time = now + timedelta(hours=3, minutes=30)
        if post.published_date <= new_time:
            post.status = True
            post.save()

    queryset = Post.objects.filter(status=False, confirm_to_post=True, trash=False)
    
