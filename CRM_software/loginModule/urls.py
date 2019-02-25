from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url('signup',views.register,name='signup'),
   # url('signup', views.SignUp.as_view(), name='signup'),
    url('home',views.home),
]