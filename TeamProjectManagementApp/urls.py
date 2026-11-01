from django.urls import path
from TeamProjectManagementApp import views

urlpatterns = [
    path('teams/', views.func1, name='teams'),
    path('membership/<int:team_id>/', views.func2, name='membership')
]