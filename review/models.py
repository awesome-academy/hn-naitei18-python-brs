import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    vote = models.FloatField()
    desc = models.TextField()
    image = models.ImageField(upload_to='book_pics')

    def __str__(self):
        return self.title


class BookMark(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    MARK_STATUS = (
        ('r', 'Readed'),
        ('n', 'Reading'),
    )
    status = models.CharField(
        max_length=1,
        choices=MARK_STATUS,
        blank=True,
        default='n',
        help_text='Book has not been read',
    )


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    REQUEST_STATUS = (
        ('rv', 'Reviewing'),
        ('a', 'Approved'),
        ('rj', 'Reject'),
    )

    status = models.CharField(
        max_length=2,
        choices=REQUEST_STATUS,
        blank=True,
        default='rv',
        help_text='Request is reviewing',
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.IntegerField()
    review = models.TextField()
    book = models.ForeignKey('Book', on_delete=models.CASCADE)


class Comment(models.Model):
    rate = models.ForeignKey(Rating, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return u'%s follows %s' % (self.follower, self.following)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ACTIVITY_TYPE = (
        ('fo', 'Follow'),
        ('fa', 'Favorite'),
        ('un_fo', 'Unfollow'),
        ('un_fa', 'Unfavorite'),
        ('ma_ed', 'Mark read'),
        ('ma_ing', 'Mark reading')
    )
    activity_type = models.CharField(
        max_length=200,
        choices=ACTIVITY_TYPE,
        blank=True,
    )
    activity = models.TextField()
