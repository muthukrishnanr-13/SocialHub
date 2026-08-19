from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Follow, Profile


@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Post.objects.create(
                author=request.user,
                content=content
            )

        return redirect('home')

    return render(request, 'social/home.html', {'posts': posts})


@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect('home')


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

    return redirect('home')


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')

    is_following = Follow.objects.filter(
        follower=request.user,
        following=user
    ).exists()

    return render(
        request,
        'social/profile.html',
        {
            'profile_user': user,
            'posts': posts,
            'is_following': is_following
        }
    )


@login_required
def follow_user(request, username):
    user_to_follow = User.objects.get(username=username)

    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            follow.delete()

    return redirect('profile', username=username)