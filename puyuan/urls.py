"""pu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from register.views import * 
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register',Register),
    path('api/auth',Login),#2
    path('api/verification/send',Send),#3
    path('api/verification/check',Check),#4
    path('api/password/forgot',Forget),#5
    path('api/password/reset',Reset),#6
    path('api/user/blood/pressure',Bloodpressure),#8
    path('api/user/weight',Weight),#9
    path('api/user/blood/sugar',Bloodsugar),#10
    path('api/user/default',Defult),#11
    path('api/user',Userinfo),#7 12 get
    path('api/user/privacy-policy',Privacy_policy),#13
    path('api/user/diary',Diary),#14
    path('api/user/diet',Diet),#15
    path('api/friend/code',Friendcode),#16
    path('api/friend/list',Friendlist),#17
    path('api/friend/requests',Friendrequest),#18
    path('api/friend/send',Friendsend),#19
    path('api/friend/<inv_id>/accept',Friendaccpet),#20 ???
    path('api/friend/<inv_id>/refuse',Friendrefuse),#21 
    path('api/friend/<uid>/remove',Invite_remove),#22
    path('api/share',Share),#23
    path('api/share/<kind>', Share0),#24
    # path('api/share/0',Share0),#24
    path('api/user/last-upload',Last_load),#25
    path('api/friend/results',Results),#26
    path('api/user/care',Care),# 27 28 
    path('api/news',NEWS),# 29
    path('api/user/medical',Medical),#30 31
    path('api/user/a1c',A1c),#32 33 34
    path('api/user/setting',Setting),#35
    path('api/notification',Notification),# 36
    path('aapi/friend/remove',Remove),#37
    path('api/register/check',Regcheck),#38
    path('api/user/badge',Badge),#39
    path('api/user/records',Dietrecord),#40 44
    path('api/user/drug-used',Drug),#41 42 43
]