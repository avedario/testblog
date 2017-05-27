#coding=utf-8

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, PostForm
from .models import Post, Category, Author, Comment, User
from django.views.generic import ListView, FormView, RedirectView, CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Posts(ListView):
    model = Post
    template_name = 'index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(Posts, self).get_context_data(**kwargs)
        posts = Post.objects.filter(status=True)
        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['page_title'] = 'Главная'
        context['posts'] = posts
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_show.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=self.get_object().pk)
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_new.html'
    success_url = reverse_lazy('account')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author_id = self.request.user
        return super(PostCreate, self).form_valid(form)


class Account(DetailView):
    model = Author
    template_name = 'account.html'
    context_object_name = 'account'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(Account, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author_id=self.request.user.id)
        return context


class HotPosts(Posts):
    template_name = 'hot.html'

    def get_context_data(self, **kwargs):
        context = super(HotPosts, self).get_context_data(**kwargs)
        context['hot_posts'] = Post.objects.filter(status=True).order_by('-rating')[:10]
        return context


class Categories(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'categories.html'


class CategoryDetail(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'category_show.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(status=True,category_id=self.get_object().pk)
        return context


class SignUp(CreateView):
    form_class = SignUpForm
    model = Author
    template_name = 'signup.html'
    success_url = reverse_lazy('index')


class Login(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return super(Login, self).form_valid(form)
        else:
            return self.form_invalid(form)


class Logout(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)
