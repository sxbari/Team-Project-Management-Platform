from django.urls import path
from TeamProjectManagementApp import views

urlpatterns = [
    path('my-teams/',views.my_teams, name = "myTeams"),
    path('explore-teams/',views.explore_teams, name = "exploreTeams"),
    
    path('me/',views.current_user, name='currentUser'),
    path('teams/', views.team_list_create, name='teams'),
    path('membership/<int:team_id>/', views.team_membership_list_create, name='membership'),
    path('csrf/', views.csrf_token_view, name='csrf'),
    path('tasks/', views.assigned_tasks_list_create, name='tasks'),
    path('register/', views.register, name='register'),
    path('login/',views.login_view, name = 'login'),
    path('logout/', views.logout_user, name='logout'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('send-request/', views.send_request, name='send_request'),
    path('teams/<int:team_id>/', views.team_data, name='team_detail'),
    path('teams/<int:team_id>/members/', views.team_members, name='team_members'),
]