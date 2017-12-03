from django.conf.urls import url

from . import views

urlpatterns = [
    # Post
    url(r'^$', views.post_list, name='post_list'),
    url(r'^create/$', views.post_create, name='post_create'),    
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<post_pk>\d+)like-toggle/$', views.post_like_toggle, name='post_like_toggle'),
    url(r'^(?P<user_id>\d+)', views.my_profile, name='my_profile'),
    
    #Comment
    url(r'^(?P<post_pk>\d+)/comment/create/$', views.comment_create, name='comment_create'),
]