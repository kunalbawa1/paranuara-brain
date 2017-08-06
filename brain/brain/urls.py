"""brain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # Get employees for the provided company name.
    url(r'^paranuara/employees', 'paranuara.views.get_empolyees'),

    # Get common friends of the provided 2 person's username.
    url(r'^paranuara/friends', 'paranuara.views.get_friends'),

    # Get the basic info for the provided person's username.
    url(r'^paranuara/person', 'paranuara.views.get_person'),
]
