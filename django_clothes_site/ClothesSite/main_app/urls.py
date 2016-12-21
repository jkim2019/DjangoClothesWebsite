from django.conf import settings
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^filter=(\w+)', views.filter, name='filter'),
    url(r'ajax_filter/', views.ajax_filter, name='ajax_filter'),
    url(r'^user/(\w+)/$', views.profile, name='profile'),
    url(r'post_url/', views.post_clothes_item, name='post_clothes_item'),
    url(r'([0-9]+)/$', views.detail, name='detail'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^favorite_clothes_item/$', views.favorite_clothes_item, name='favorite_clothes_item'),
    url(r'^unfavorite_clothes_item/$', views.unfavorite_clothes_item, name='unfavorite_clothes_item'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^signup/$', views.UserFormView.as_view(), name='signup'),
]




