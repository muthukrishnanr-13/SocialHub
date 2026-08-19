from django.db import models
from django.contrib.auth.models import User


# =========================================================
# PROFILE
# =========================================================

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    bio = models.TextField(
        blank=True,
        default=''
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username


# =========================================================
# POST
# =========================================================

class Post(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.author.username} - {self.content[:30]}"


# =========================================================
# LIKE
# =========================================================

class Like(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                name='unique_post_like'
            )
        ]

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"


# =========================================================
# COMMENT
# =========================================================

class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"


# =========================================================
# FOLLOW
# =========================================================

class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return (
            f"{self.follower.username} "
            f"follows "
            f"{self.following.username}"
        )


# =========================================================
# NOTIFICATION
# =========================================================

class Notification(models.Model):

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.sender.username} -> "
            f"{self.recipient.username}: "
            f"{self.message}"
        )