from django.urls import path, include
from django.conf.urls import url

from . import views

app_name= 'chat'

urlpatterns = [
    path('entry', views.entry, name='entry'),
    path('<str:room_name>/', views.room, name='room'),

]
