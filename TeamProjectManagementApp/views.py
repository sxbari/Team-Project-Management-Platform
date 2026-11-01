from django.shortcuts import render
from TeamProjectManagementApp.models import Team, Membership
from django.http import JsonResponse
# Create your views here.

def func1(request):
    if request.method == "GET":
        data =list(Team.objects.all().values())
        return JsonResponse(data, safe=False)

def func2(request,team_id):
    if request.method == "GET":
        data = list(Membership.objects.filter(team_id=team_id).values())
        return JsonResponse(data, safe=False)