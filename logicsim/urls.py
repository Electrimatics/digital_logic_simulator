from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name = 'index'),
    path('createGate/', views.createGate, name='createGate'),
    path('add/',views.add, name='add')


]