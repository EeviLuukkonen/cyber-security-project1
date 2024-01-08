from django.urls import path

from .views import index, login_redirect, detail, create_blog

urlpatterns = [
    path('', index, name='index'),
    path('<int:blog_id>/', detail, name='detail'),
    path('create/', create_blog, name='create_blog'),
    path('login_redirect/', login_redirect, name='login_redirect'),
]