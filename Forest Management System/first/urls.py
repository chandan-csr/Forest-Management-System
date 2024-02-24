"""first URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.http.response import HttpResponseNotAllowed
from django.urls import path
from hello.views import home,user,uuser,login,ulogin,orders,order,uorder,orderhistory,uorderhistory,upass,uupass,userpart
from hello.views import sendSimpleEmail,getotp,cpass,changepass
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('home/', home),
    path('user/', user),
    path('uuser/', uuser),
    path('login/', login),
    path('ulogin/', ulogin),
    path('userpart/', userpart),
    path('upass/', upass),
    path('uupass/', uupass),
    path('orders/', orders),
    path('order/', order),
    path('uorder/', uorder),
    path('orderhistory/', orderhistory),
    path('uorderhistory/', uorderhistory),
    path('SM/',sendSimpleEmail),
    path('getotp/',getotp),
    path('cpass/',cpass),
    path('changepass/',changepass)
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)