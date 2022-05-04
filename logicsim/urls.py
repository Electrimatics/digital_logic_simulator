from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name = 'index'),
    path('createGate/', views.createGate, name='createGate'),
    path('add/',views.add, name='add'),
    path('update/<int:gate_id>', views.update, name='update'),
    path('delete/<int:gate_id>', views.delete, name='delete')

]