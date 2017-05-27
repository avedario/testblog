import os
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Author(User):
    rating = models.IntegerField(default=0)


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    category_id = models.ForeignKey(Category, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    rating = models.IntegerField(default=0) 
    author_id = models.ForeignKey(User, default=0, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post_id = models.ForeignKey(Post, default=0)
    author_id = models.ForeignKey(User, default=0)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
