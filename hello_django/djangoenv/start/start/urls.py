"""
URL configuration for start project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from hello import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.main, name='main'),
    path('stats/', views.stats, name='stats'),
    path('admin/', admin.site.urls),
    path('about_company/',views.about_company),
    path('contacts/',views.contacts),
    path('news/',views.news),
    path('politics/',views.politics),
    path('promocodes/',views.promocodes),
    path('qa/',views.qa),
    path('reviews/',views.reviews),
    path('vacancies/',views.vacancies),
    path('statistics/',views.statisticsv),
    path('logout/', views.logout, name='logout'),

    path('register/master/<int:master_id>',views.mastersview, name="master"),
    path('login/master/<int:master_id>',views.mastersview, name="master"),
    path('register/client/<int:client_id>',views.clientsview, name="client"),
    path('login/client/<int:client_id>',views.clientsview, name="client"),
    path('register/',views.register),
    path('login/',views.login),

    re_path(r'^(login|register)/master/editmaster/(?P<master_id>\d+)', views.editmaster, name="editmaster"),
    re_path(r'^(login|register)/client/editclient/(?P<client_id>\d+)', views.editclient, name="editclient"),

    re_path(r'^(login|register)/client/createorder/(?P<client_id>\d+)', views.createorder, name="createorder"),

    
    re_path(r'^(login|register)/client/editreview/(?P<client_id>\d+)/(?P<review_id>\d+)', views.editreview, name="editreview"),
    re_path(r'^(login|register)/client/deletereview/(?P<client_id>\d+)/(?P<review_id>\d+)', views.deletereview, name="deletereview"),
    re_path(r'^(login|register)/client/createreview/(?P<client_id>\d+)', views.createreview, name="createreview"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)