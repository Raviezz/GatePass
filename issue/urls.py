from issue import views

__author__ = 'Raviteja'
from django.conf.urls import url

urlpatterns = [
    url(r'^home/', views.home, name="home"),

]
