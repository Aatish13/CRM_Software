from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url('dashboard', views.dashboard),
    url('employees', views.display_employees),
]