from django.urls import path

from schedule import views

"""
This module contains the URL patterns for the schedule app.
"""

urlpatterns = [
    path('', views.index, name='index'),
    path('positions_list/<int:user_id>/', views.positions_list, name='positions_list'),
    path('add_construction_name/<int:user_id>/', views.add_construction_name, name='add_construction_name'),
    path('edit_construction_name/<int:user_id>/<int:pk>/', views.edit_construction_name, name='edit_construction_name'),
    path('delete_construction_name/<int:user_id>/<int:pk>/', views.delete_construction_name,
         name='delete_construction_name'),
    path('add/<int:user_id>/', views.add_position, name='add_position'),
    path('edit/<int:user_id>/<int:pk>/', views.edit_position, name='edit_position'),
    path('delete/<int:user_id>/<int:pk>/', views.delete_position, name='delete_position'),
    path('schedule/<int:user_id>/', views.schedule, name='schedule'),
]