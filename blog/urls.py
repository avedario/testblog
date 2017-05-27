from django.conf.urls import url
from .views import Posts, PostDetail, HotPosts, Categories, Login, Logout, SignUp,\
                   CategoryDetail, PostCreate, Account
from . import views

urlpatterns = [
    url(r'^$', Posts.as_view(), name='index'),
    url(r'^post/create/$', PostCreate.as_view(), name='post_create'),
    url(r'^post/(?P<slug>[a-zA-Z0-9\_\.]+)/$', PostDetail.as_view(), name='post_show'),
    url(r'^hot/$', HotPosts.as_view(), name='hot'),
    url(r'^categories/$', Categories.as_view(), name='categories'),
    url(r'^category/(?P<slug>[a-zA-Z0-9\_\.]+)/$', CategoryDetail.as_view(), name='category_show'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^account/$', Account.as_view(), name='account'),
]