from django.urls import path
from TeamProjectManagementApp import views

urlpatterns = [
    path('my-teams/',views.my_teams, name = "myTeams"),
    path('explore-teams/',views.explore_teams, name = "exploreTeams"),
    
    path('me/',views.current_user, name='currentUser'),
    path('teams/', views.func1, name='teams'),
    path('membership/<int:team_id>/', views.func2, name='membership'),
    path('csrf/', views.csrf_token_view, name='csrf'),
    path('tasks/', views.func3, name='tasks'),
    path('register/', views.register, name='register'),
    path('login/',views.login_view, name = 'login')
]