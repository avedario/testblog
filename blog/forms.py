from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Comment, Post


class SignUpForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ('username', 'first_name', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['created_at', 'rating', 'author_id']
