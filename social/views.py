from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from .forms import RegisterForm
from .models import (
    Post,
    Comment,
    Like,
    Follow,
    Profile,
    Notification
)


# =========================================================
# HOME
# =========================================================

@login_required
def home(request):

    if request.method == 'POST':

        content = request.POST.get('content', '').strip()

        if content:
            Post.objects.create(
                author=request.user,
                content=content
            )

        return redirect('home')

    posts = (
        Post.objects
        .select_related('author')
        .prefetch_related('likes', 'comments__author')
        .order_by('-created_at')
    )

    return render(
        request,
        'social/home.html',
        {
            'posts': posts
        }
    )


# =========================================================
# LIKE / UNLIKE POST
# =========================================================

@login_required
def like_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like = Like.objects.filter(
        post=post,
        user=request.user
    ).first()

    if like:

        # Already liked -> Unlike
        like.delete()

    else:

        # Like the post
        Like.objects.create(
            post=post,
            user=request.user
        )

        # Notification only for another user
        if post.author != request.user:

            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                message=(
                    f"{request.user.username} "
                    f"liked your post."
                )
            )

    return redirect('home')


# =========================================================
# DELETE POST
# =========================================================

@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    # Only post owner can delete
    if post.author == request.user:
        post.delete()

    return redirect('home')


# =========================================================
# ADD COMMENT
# =========================================================

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.method == 'POST':

        content = request.POST.get(
            'content',
            ''
        ).strip()

        if content:

            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

            # Don't notify yourself
            if post.author != request.user:

                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    message=(
                        f"{request.user.username} "
                        f"commented on your post."
                    )
                )

    return redirect('home')


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    posts = (
        Post.objects
        .filter(author=profile_user)
        .prefetch_related('likes', 'comments__author')
        .order_by('-created_at')
    )

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    return render(
        request,
        'social/profile.html',
        {
            'profile_user': profile_user,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'is_following': is_following,
        }
    )


# =========================================================
# FOLLOW / UNFOLLOW
# =========================================================

@login_required
def follow_user(request, username):

    user_to_follow = get_object_or_404(
        User,
        username=username
    )

    # User cannot follow himself
    if user_to_follow == request.user:
        return redirect(
            'profile',
            username=username
        )

    follow = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    ).first()

    if follow:

        # Already following -> Unfollow
        follow.delete()

    else:

        # Follow
        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )

        # Notification
        Notification.objects.create(
            recipient=user_to_follow,
            sender=request.user,
            message=(
                f"{request.user.username} "
                f"started following you."
            )
        )

    return redirect(
        'profile',
        username=username
    )


# =========================================================
# FOLLOWERS
# =========================================================

@login_required
def followers(request, username):

    user = get_object_or_404(
        User,
        username=username
    )

    follow_objects = (
        Follow.objects
        .filter(following=user)
        .select_related('follower')
        .order_by('-created_at')
    )

    users = [
        follow.follower
        for follow in follow_objects
    ]

    return render(
        request,
        'social/followers.html',
        {
            'profile_user': user,
            'users': users,
            'title': 'Followers'
        }
    )


# =========================================================
# FOLLOWING
# =========================================================

@login_required
def following(request, username):

    user = get_object_or_404(
        User,
        username=username
    )

    follow_objects = (
        Follow.objects
        .filter(follower=user)
        .select_related('following')
        .order_by('-created_at')
    )

    users = [
        follow.following
        for follow in follow_objects
    ]

    return render(
        request,
        'social/followers.html',
        {
            'profile_user': user,
            'users': users,
            'title': 'Following'
        }
    )


# =========================================================
# NOTIFICATIONS
# =========================================================

@login_required
def notifications(request):

    notifications_list = (
        Notification.objects
        .filter(recipient=request.user)
        .select_related('sender')
        .order_by('-created_at')
    )

    # Mark unread notifications as read
    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        'social/notifications.html',
        {
            'notifications': notifications_list
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(
                commit=False
            )

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            # Create profile if it doesn't exist
            Profile.objects.get_or_create(
                user=user
            )

            login(
                request,
                user
            )

            return redirect('home')

    else:

        form = RegisterForm()

    return render(
        request,
        'social/register.html',
        {
            'form': form
        }
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect('home')

        return render(
            request,
            'social/login.html',
            {
                'error': 'Invalid username or password'
            }
        )

    return render(
        request,
        'social/login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect('login') 