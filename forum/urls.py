from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]