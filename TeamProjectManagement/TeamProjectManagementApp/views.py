import json
from django.contrib.auth.models import User   
from TeamProjectManagementApp.models import Tasks, Team, Membership
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return JsonResponse({"error": "All Fields are required"},status = 401)
        elif User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username Exists Already"}, status=401)
        elif User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already Exists"}, status = 401)
        
        User.objects.create_user(username=username,email=email,password=password)
        return JsonResponse({"message": "User created successfully!"}, status = 201)


def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return JsonResponse({"message":"Login Successfull"},status = 201)
        else:
            return JsonResponse({"message":"Invalid Login Credentials"},status = 401)
    else:
        return JsonResponse({"message":"Method Not Allowed"},status = 405)

def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})

def func1(request):
    if request.method == "GET":
        data =list(Team.objects.all().values())
        return JsonResponse(data, safe=False)
    
    if request.method == "POST":
        data = json.loads(request.body)
        team_name = data.get('team_name')
        description = data.get('description')
        Team.objects.create(team_name=team_name, description=description)    
        return JsonResponse({"message": "Object created successfully!"}, status=201)


def func2(request, team_id):
    if request.method == "GET":
        data = list(Membership.objects.filter(team_id=team_id).values())
        return JsonResponse(data, safe=False)

    if request.method == "POST":

        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required"}, status=401)

        user_id = request.user.id

        if not Team.objects.filter(id=team_id).exists():
            return JsonResponse({"error": "Team not found"}, status=404)

        if Membership.objects.filter(user_id=user_id, team_id=team_id).exists():
            return JsonResponse({"error": "Membership already exists"}, status=409)

        Membership.objects.create(
            user_id=user_id,
            team_id=team_id,
            role="member",
            status="pending"
        )

        return JsonResponse(
            {"message": "Membership request created successfully!"},
            status=201
        )

    return JsonResponse({"error": "Method not allowed"}, status=405)

def func3(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"error":"login required"},status = 401)
        data = list(Tasks.objects.filter(assigned_to=request.user).values())
        return JsonResponse(data, safe=False)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"error":"login required"},status = 401)
        
        data = json.loads(request.body)
        task_name = data.get('task_name')
        description = data.get('description')
        team_id = data.get('team_id')
        deadline = data.get('deadline')
        Tasks.objects.create(
            task_name=task_name,
            description=description,
            team_id=team_id,
            assigned_to=request.user,
            deadline=deadline,
            priority=data.get('priority')
        )
        return JsonResponse({"message": "Task created successfully!"}, status=201)
    
    def __str__(self):
        return self.task_name
    
def current_user(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error":"Not Authenticated"},status=401
        )
    return JsonResponse({
        "id":request.user.id,
        "username":request.user.username,
        "email":request.user.email
    })
def my_teams(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "User not Authenticated"}, status=401
        )
    memberships = Membership.objects.filter(
        user=request.user,
        status="approved"
    )
    teams = []
    for membership in memberships:
        teams.append({
            "team_id": membership.team.id,
            "team_name": membership.team.team_name,
            "team_description": membership.team.description,
            "role": membership.role,
            "joined_at": membership.joined_at
        })
    
    return JsonResponse({"teams":teams})

def explore_teams(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error":"User not Authenticated"}
        )
    existing_teams = Membership.objects.filter(
        user = request.user).values_list("team_id",flat=True)

    teams = Team.objects.filter(is_active =True).exclude(
        id_in = existing_teams
    )

    teams_list = []
    for team in teams:
        teams_list.append({
            "team_id":team.id,
            "team_name":team.team_name,
            "team_description":team.description,
            "created_at":team.created_at
        })
    return JsonResponse(
        {"teams":teams_list}
    )

def my_requests(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error":"Unatuhorised"}
             )
    join_status = []
    records = Membership.objects.filter(user=request.user)
    for req in records:
            join_status.append(
                {"team_name":req.team.name,
                 "status":req.status}
            )
    return JsonResponse(
        {"requests":join_status}
    )

def send_request(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error":"Unauthenticated"},status=401
        )
    data = json.loads(request.body)
    team_id = data.get("team_id")

  
    if Membership.objects.filter(user=request.user,team_id=team_id,status="pending").exists():
        return JsonResponse(
            {
                "error":"Request already Pending"
            }
        )
    if not Team.objects.filter(team_id=team_id,is_acive =True).exists():
        return JsonResponse(
            {
                "error":"Team inactive"
            }
        )
    Membership.objects.create(
        user = request.user,
        team_id = team_id,
        role = "member",
        status = "pending"
    )
    return JsonResponse(
        {"message":"Request sent successfully"},status=201
    )