from django.contrib.auth import login, logout

__author__ = 'Raviteja'
from django.conf.urls import url
from approve import views

urlpatterns = [
    url(r'^home/', views.home, name="home"),

]
