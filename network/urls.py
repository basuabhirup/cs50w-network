
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/<str:username>', views.profile, name='profile'),
    path('following', views.following_posts, name='following_posts'),
    
    # API Routes
    path("posts", views.posts, name="posts"),
    path("posts/<int:post_id>", views.edit_post, name="edit_post"),
    path("follow/<str:username>", views.follow, name='follow'),
    path('like/<int:post_id>', views.like, name='like')
]
