from django.conf.urls import url
from . import views

urlpatterns = [ 
                       
     url(r'^login/$', views.user_login, name='login'),
     
     url(r'^authenticate_user/$', views.authenticate_user, name='login'),
     
#      url(r'^authenticate_user/(?P<reg>\w{0,100}[-\w|\w|\W]+)/$', views.authenticate_user, name='login'),
     
     url(r'^logout/$', views.user_logout, name='logout'),
     
     url(r'^register/$', views.request_registration, name='request_registration'),
     
     url(r'^approve_user/$', views.approve_user, name='approve_user'),
     
     url(r'^add_user/$', views.add_user, name='add_user'),
     
     url(r'^delete_user/$', views.delete_user, name='delete_user'),
]