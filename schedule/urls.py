from django.urls import path

from schedule import views

"""
This module contains the URL patterns for the schedule app.
"""

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('constructions_list/<int:user_id>/', views.ConstructionListView.as_view(), name='constructions_list'),
    path('add/<int:user_id>/', views.AddConstructionView.as_view(), name='add_construction'),
    path('edit/<int:user_id>/<int:construction_id>/', views.EditConstructionView.as_view(), name='edit_construction'),
    path('delete/<int:user_id>/<int:construction_id>/', views.DeleteConstructionView.as_view(),
         name='delete_construction'),
    path('positions_list/<int:user_id>/<int:construction_id>/', views.PositionsListView.as_view(),
         name='positions_list'),
    path('add/<int:user_id>/<int:construction_id>/', views.AddPositionView.as_view(), name='add_position'),
    path('edit/<int:user_id>/<int:construction_id>/<int:position_id>/', views.EditPositionView.as_view(),
         name='edit_position'),
    path('delete/<int:user_id>/<int:construction_id>/<int:position_id>/', views.DeletePositionView.as_view(),
         name='delete_position'),
    path('schedule/<int:user_id>/<int:construction_id>/', views.ScheduleView.as_view(), name='schedule'),
]
