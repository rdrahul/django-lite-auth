from django.conf.urls import url
from . import views
urlpatterns= [
    
    url('^$', views.home, name = "home" ),
    url('^login/(?P<backend>\w+)$', views.login, name = "login" ),
    url('^logout$', views.logout, name= "logout" ),
    url('^redirect$', views.redirect, name= "redirect" ),

]      