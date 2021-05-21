from django.urls import path

from . import views

urlpatterns = [
    path('add', views.add_posts, name='add_posts'),
    path('update/<int:post_id>', views.update_post, name='published'),
    path('ping', views.ping, name='ping'),
]
