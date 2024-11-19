from django.urls import include, path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('api/v1/', include('blog.api.v1.urls')), 

]
