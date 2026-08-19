from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # HOME
    # =========================

    path('', views.home, name='home'),


    # =========================
    # AUTHENTICATION
    # =========================

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),


    # =========================
    # POSTS
    # =========================

    path(
        'like/<int:post_id>/',
        views.like_post,
        name='like_post'
    ),

    path(
        'delete/<int:post_id>/',
        views.delete_post,
        name='delete_post'
    ),

    path(
        'comment/<int:post_id>/',
        views.add_comment,
        name='add_comment'
    ),


    # =========================
    # PROFILE
    # =========================

    path(
        'profile/<str:username>/',
        views.profile,
        name='profile'
    ),

    path(
        'follow/<str:username>/',
        views.follow_user,
        name='follow_user'
    ),


    # =========================
    # FOLLOWERS / FOLLOWING
    # =========================

    path(
        'profile/<str:username>/followers/',
        views.followers,
        name='followers'
    ),

    path(
        'profile/<str:username>/following/',
        views.following,
        name='following'
    ),


    # =========================
    # NOTIFICATIONS
    # =========================

    path(
        'notifications/',
        views.notifications,
        name='notifications'
    ),

]