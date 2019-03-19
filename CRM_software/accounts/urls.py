from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url('signup',views.register,name='signup'),
   # url('signup', views.SignUp.as_view(), name='signup'),
    url('home',views.home),
    url('login', views.login),
    url('viewinfo', views.viewProfile),
    url('info', views.info),
    url('delete', views.delete),
    url('changePass', views.changePass),
    url('processChange',views.processChange),
    url('update', views.update),
    url('changePass', views.changePass),
    url('processChange',views.processChange),
    url(r'^auth/$', views.auth_view),
    url(r'^logout/$', views.logout),
    url(r'^loggedin/$', views.loggedin),
    url(r'^invalidlogin/$', views.invalidlogin),
]