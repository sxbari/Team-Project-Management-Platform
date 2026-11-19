import json
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from TeamProjectManagementApp.models import (
    ActivityLog,
    Attachment,
    Comment,
    Meeting,
    Membership,
    Notification,
    Task,
    TaskSubmission,
    Team,
)
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout 
# Create your views here.

def register(request):
    if request.method == "POST":
        data, error = _read_json_body(request)
        if error:
            return error
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return JsonResponse({"error": "All Fields are required"},status = 400)
        elif User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username Exists Already"}, status=400)
        elif User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already Exists"}, status = 400)
        
        User.objects.create_user(username=username,email=email,password=password)
        return JsonResponse({"message": "User created successfully!"}, status = 201)
    return JsonResponse({"error": "Method not allowed"}, status=405)


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

def team_list_create(request):
    if request.method == "GET":
        data =list(Team.objects.all().values())
        return JsonResponse(data, safe=False)
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required"}, status=401)
        data, error = _read_json_body(request)
        if error:
            return error
        team_name = data.get('team_name')
        description = data.get('description')
        if not team_name or not description:
            return JsonResponse(
                {"error": "team_name and description are required"},
                status=400,
            )
        with transaction.atomic():
            team = Team.objects.create(
                team_name=team_name,
                description=description,
            )
            Membership.objects.create(
                user=request.user,
                team=team,
                role="leader",
                status="approved",
            )
        return JsonResponse({"message": "Object created successfully!"}, status=201)


def team_membership_list_create(request, team_id):
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

def assigned_tasks_list_create(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"error":"login required"},status = 401)
        data = list(Task.objects.filter(assigned_to=request.user).values())
        return JsonResponse(data, safe=False)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"error":"login required"},status = 401)
        
        data, error = _read_json_body(request)
        if error:
            return error
        task_name = data.get('task_name')
        description = data.get('description')
        team_id = data.get('team_id')
        deadline = data.get('deadline')
        parsed_deadline, error = _parse_datetime_field(deadline, 'deadline')
        if error:
            return error
        priority = data.get('priority')
        if priority not in dict(Task.PRIORITY_CHOICES):
            return JsonResponse({"error": "Invalid task priority"}, status=400)
        Task.objects.create(
            task_name=task_name,
            description=description,
            team_id=team_id,
            assigned_to=request.user,
            created_by=request.user,
            deadline=parsed_deadline,
            priority=priority
        )
        return JsonResponse({"message": "Task created successfully!"}, status=201)
    
    
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
        id__in = existing_teams
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
            {"error":"Unauthorised"},status=401
             )
    join_status = []
    records = Membership.objects.filter(user=request.user)
    for req in records:
            join_status.append(
                {"team_name":req.team.team_name,
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
    if not Team.objects.filter(id=team_id,is_active=True).exists():
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

def logout_user(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "error":"Unauthenticated"
            },status=401
        )
    logout(request)
    return JsonResponse(
        {
            "message":"Logout Successfully!"
        },status=200
    )

def team_data(request,team_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "error":"Unauthenticated"
            },status=401
        )
    try:
        data = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return JsonResponse(
            {
                "error":"No Team Exists on with that ID."
            },status=404
        ) 
    team_name = data.team_name
    team_desc= data.description
    team_creationtime = data.created_at
    team_status = data.is_active
    team_details = {
        "team_name":team_name,
        "team_description":team_desc,
        "team_creation_time":team_creationtime,
        "team_status": team_status
        }

    return JsonResponse(
        {
            "message":team_details
        },status=200
    )

def team_members(request,team_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "error":"Unauthenticated"
            },status=401
        )
    data = Membership.objects.filter(team_id=team_id,
                                     status="approved")
    member_detail = []
    for person in data:
        teamMember = person.user.username
        role = person.role 
        joined = person.joined_at
        member_detail.append({
            "username":teamMember,
            "role":role,
            "joining date":joined
        })

    return JsonResponse(
        {
            "details":member_detail
        },status=200
    )
def member_leave(request,team_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "error":"Unauthorised"
            },status=401
        )
    try:

        data = Membership.objects.get(team_id=team_id,user=request.user)
    except Membership.DoesNotExist:
        return JsonResponse(
            {
                "error":"User is not a part of that team"
            },status=401
        )
    if data.status != "left":
        data.status = "left"
        data.save()
    else:
        return JsonResponse(
            {
                "error":"User not a Part"
            },status=401
        )
    return JsonResponse(
        {
            "message":"Successfully Left the team"
        },status=200
    )


def _read_json_body(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, JsonResponse({"error": "Invalid JSON body"}, status=400)
    if not isinstance(data, dict):
        return None, JsonResponse({"error": "A JSON object is required"}, status=400)
    return data, None


def _require_team_access(request, team_id, leader=False):
    if not request.user.is_authenticated:
        return None, JsonResponse({"error": "Login required"}, status=401)

    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return None, JsonResponse({"error": "Team not found"}, status=404)

    membership = Membership.objects.filter(
        user=request.user,
        team=team,
        status="approved",
    ).first()
    if membership is None:
        return None, JsonResponse({"error": "Approved team membership required"}, status=403)
    if leader and membership.role.lower() != "leader":
        return None, JsonResponse({"error": "Team leader access required"}, status=403)
    return team, None


def _require_task_access(request, task_id):
    if not request.user.is_authenticated:
        return None, JsonResponse({"error": "Login required"}, status=401)

    task = Task.objects.select_related("team", "assigned_to", "created_by").filter(
        id=task_id
    ).first()
    if task is None:
        return None, JsonResponse({"error": "Task not found"}, status=404)

    _, error = _require_team_access(request, task.team_id)
    return (None, error) if error else (task, None)


def _task_json(task):
    return {
        "id": task.id,
        "task_name": task.task_name,
        "description": task.description,
        "team_id": task.team_id,
        "assigned_to": task.assigned_to_id,
        "assigned_to_username": (
            task.assigned_to.username if task.assigned_to else None
        ),
        "created_by": task.created_by_id,
        "created_at": task.created_at,
        "deadline": task.deadline,
        "completed_at": task.completed_at,
        "status": task.status,
        "priority": task.priority,
    }


def _meeting_json(meeting):
    return {
        "id": meeting.id,
        "team_id": meeting.team_id,
        "title": meeting.title,
        "description": meeting.description,
        "scheduled_at": meeting.scheduled_at,
        "meeting_link": meeting.meeting_link,
        "created_by": meeting.created_by_id,
        "status": meeting.status,
        "created_at": meeting.created_at,
        "updated_at": meeting.updated_at,
    }


def _record_activity(team, user, action, description, task=None):
    ActivityLog.objects.create(
        team=team,
        user=user,
        task=task,
        action=action,
        description=description,
    )


def _parse_datetime_field(value, field_name):
    parsed = parse_datetime(value) if isinstance(value, str) else None
    if parsed is None:
        return None, JsonResponse(
            {"error": f"{field_name} must be a valid ISO-8601 datetime"},
            status=400,
        )
    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed, None


def _is_positive_integer(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def team_activity(request, team_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    team, error = _require_team_access(request, team_id)
    if error:
        return error
    activities = ActivityLog.objects.filter(team=team).select_related("user", "task")
    return JsonResponse({
        "activities": [
            {
                "id": item.id,
                "user_id": item.user_id,
                "username": item.user.username if item.user else None,
                "task_id": item.task_id,
                "action": item.action,
                "description": item.description,
                "created_at": item.created_at,
            }
            for item in activities
        ]
    })


def team_join_requests(request, team_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    team, error = _require_team_access(request, team_id, leader=True)
    if error:
        return error
    requests = Membership.objects.filter(
        team=team,
        status="pending",
    ).select_related("user")
    return JsonResponse({
        "requests": [
            {
                "id": item.id,
                "user_id": item.user_id,
                "username": item.user.username,
                "role": item.role,
                "status": item.status,
                "joined_at": item.joined_at,
            }
            for item in requests
        ]
    })


def review_join_request(request, membership_id, decision):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if decision not in ("approved", "rejected"):
        return JsonResponse({"error": "Invalid join request action"}, status=400)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    membership = Membership.objects.select_related("team", "user").filter(
        id=membership_id
    ).first()
    if membership is None:
        return JsonResponse({"error": "Membership request not found"}, status=404)
    _, error = _require_team_access(request, membership.team_id, leader=True)
    if error:
        return error
    if membership.status != "pending":
        return JsonResponse({"error": "Membership request is no longer pending"}, status=409)

    membership.status = decision
    membership.save(update_fields=["status"])
    action = "join_request_approved" if decision == "approved" else "join_request_rejected"
    _record_activity(
        membership.team,
        request.user,
        action,
        f"{request.user.username} {decision} {membership.user.username}'s join request.",
    )
    return JsonResponse({"message": f"Join request {decision}"})


def approve_join_request(request, membership_id):
    return review_join_request(request, membership_id, "approved")


def reject_join_request(request, membership_id):
    return review_join_request(request, membership_id, "rejected")


def remove_team_member(request, team_id, membership_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    team, error = _require_team_access(request, team_id, leader=True)
    if error:
        return error
    membership = Membership.objects.select_related("user").filter(
        id=membership_id,
        team=team,
        status="approved",
    ).first()
    if membership is None:
        return JsonResponse({"error": "Active team member not found"}, status=404)
    if membership.role.lower() == "leader":
        return JsonResponse({"error": "A team leader cannot be removed"}, status=400)
    member_username = membership.user.username
    membership.status = "left"
    membership.save(update_fields=["status"])
    _record_activity(
        team,
        request.user,
        "member_removed",
        f"{member_username} was removed from the team.",
    )
    return JsonResponse({"message": "Member removed"})


def my_tasks(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)
    tasks = Task.objects.filter(assigned_to=request.user).select_related(
        "team", "assigned_to", "created_by"
    ).order_by("deadline", "id")
    return JsonResponse({"tasks": [_task_json(task) for task in tasks]})


def task_history(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)
    tasks = Task.objects.filter(
        assigned_to=request.user,
        status="completed",
    ).select_related("team", "assigned_to", "created_by").order_by(
        "-completed_at", "-id"
    )
    return JsonResponse({"tasks": [_task_json(task) for task in tasks]})


def team_tasks(request, team_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    team, error = _require_team_access(request, team_id)
    if error:
        return error
    tasks = Task.objects.filter(team=team).select_related(
        "team", "assigned_to", "created_by"
    ).order_by("deadline", "id")
    return JsonResponse({"tasks": [_task_json(task) for task in tasks]})


def create_team_task(request, team_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    team, error = _require_team_access(request, team_id, leader=True)
    if error:
        return error
    data, error = _read_json_body(request)
    if error:
        return error
    task_name = data.get("task_name")
    description = data.get("description")
    if not isinstance(task_name, str) or not task_name.strip():
        return JsonResponse({"error": "task_name is required"}, status=400)
    if not isinstance(description, str) or not description.strip():
        return JsonResponse({"error": "description is required"}, status=400)
    deadline, error = _parse_datetime_field(data.get("deadline"), "deadline")
    if error:
        return error

    priority = data.get("priority", "medium")
    if priority not in dict(Task.PRIORITY_CHOICES):
        return JsonResponse({"error": "Invalid task priority"}, status=400)
    assigned_to_id = data.get("assigned_to")
    assigned_user = None
    if assigned_to_id is not None:
        if not _is_positive_integer(assigned_to_id):
            return JsonResponse({"error": "assigned_to must be a user ID or null"}, status=400)
        assigned_user = User.objects.filter(
            id=assigned_to_id,
            memberships__team=team,
            memberships__status="approved",
        ).first()
        if assigned_user is None:
            return JsonResponse(
                {"error": "Assignee must be an approved team member"},
                status=400,
            )

    task = Task.objects.create(
        task_name=task_name.strip(),
        description=description.strip(),
        team=team,
        assigned_to=assigned_user,
        created_by=request.user,
        deadline=deadline,
        priority=priority,
    )
    _record_activity(
        team,
        request.user,
        "task_created",
        f"{request.user.username} created task '{task.task_name}'.",
        task,
    )
    return JsonResponse(_task_json(task), status=201)


def task_detail(request, task_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    task, error = _require_task_access(request, task_id)
    if error:
        return error
    result = _task_json(task)
    result["submissions"] = [
        {
            "id": submission.id,
            "submitted_by": submission.submitted_by_id,
            "submitted_at": submission.submitted_at,
            "description": submission.description,
            "review_status": submission.review_status,
            "feedback": submission.feedback,
        }
        for submission in task.submissions.select_related("submitted_by").order_by(
            "-submitted_at"
        )
    ]
    return JsonResponse(result)


def update_task(request, task_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    task, error = _require_task_access(request, task_id)
    if error:
        return error
    _, error = _require_team_access(request, task.team_id, leader=True)
    if error:
        return error
    data, error = _read_json_body(request)
    if error:
        return error

    if "task_name" in data:
        if not isinstance(data["task_name"], str) or not data["task_name"].strip():
            return JsonResponse({"error": "task_name cannot be empty"}, status=400)
        task.task_name = data["task_name"].strip()
    if "description" in data:
        if not isinstance(data["description"], str) or not data["description"].strip():
            return JsonResponse({"error": "description cannot be empty"}, status=400)
        task.description = data["description"].strip()
    if "deadline" in data:
        task.deadline, error = _parse_datetime_field(data["deadline"], "deadline")
        if error:
            return error
    if "priority" in data:
        if data["priority"] not in dict(Task.PRIORITY_CHOICES):
            return JsonResponse({"error": "Invalid task priority"}, status=400)
        task.priority = data["priority"]
    task.save()
    _record_activity(
        task.team,
        request.user,
        "task_updated",
        f"{request.user.username} updated task '{task.task_name}'.",
        task,
    )
    return JsonResponse(_task_json(task))


def assign_task(request, task_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    task, error = _require_task_access(request, task_id)
    if error:
        return error
    _, error = _require_team_access(request, task.team_id, leader=True)
    if error:
        return error
    data, error = _read_json_body(request)
    if error:
        return error
    if "user_id" not in data:
        return JsonResponse({"error": "user_id is required (or null to unassign)"}, status=400)

    assigned_user = None
    if data["user_id"] is not None:
        if not _is_positive_integer(data["user_id"]):
            return JsonResponse({"error": "user_id must be a user ID or null"}, status=400)
        assigned_user = User.objects.filter(
            id=data["user_id"],
            memberships__team=task.team,
            memberships__status="approved",
        ).first()
        if assigned_user is None:
            return JsonResponse(
                {"error": "Assignee must be an approved team member"},
                status=400,
            )
    task.assigned_to = assigned_user
    task.save(update_fields=["assigned_to"])
    _record_activity(
        task.team,
        request.user,
        "task_assigned",
        f"{request.user.username} changed the assignee for '{task.task_name}'.",
        task,
    )
    return JsonResponse(_task_json(task))


def update_task_status(request, task_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    task, error = _require_task_access(request, task_id)
    if error:
        return error
    is_leader = Membership.objects.filter(
        user=request.user,
        team=task.team,
        status="approved",
        role__iexact="leader",
    ).exists()
    if task.assigned_to_id != request.user.id and not is_leader:
        return JsonResponse({"error": "Only the assignee or team leader may update status"}, status=403)
    data, error = _read_json_body(request)
    if error:
        return error
    status = data.get("status")
    if status not in dict(Task.STATUS_CHOICES):
        return JsonResponse({"error": "Invalid task status"}, status=400)
    task.status = status
    task.completed_at = timezone.now() if status == "completed" else None
    task.save(update_fields=["status", "completed_at"])
    _record_activity(
        task.team,
        request.user,
        "task_status_updated",
        f"{request.user.username} changed '{task.task_name}' to {status}.",
        task,
    )
    return JsonResponse(_task_json(task))


def submit_task(request, task_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    task, error = _require_task_access(request, task_id)
    if error:
        return error
    if task.assigned_to_id != request.user.id:
        return JsonResponse({"error": "Only the assignee may submit this task"}, status=403)
    data, error = _read_json_body(request)
    if error:
        return error
    description = data.get("description", "")
    if not isinstance(description, str):
        return JsonResponse({"error": "description must be a string"}, status=400)
    if task.submissions.filter(review_status="pending").exists():
        return JsonResponse({"error": "A submission is already awaiting review"}, status=409)
    submission = TaskSubmission.objects.create(
        task=task,
        submitted_by=request.user,
        description=description,
    )
    task.status = "completed"
    task.completed_at = timezone.now()
    task.save(update_fields=["status", "completed_at"])
    _record_activity(
        task.team,
        request.user,
        "task_submitted",
        f"{request.user.username} submitted '{task.task_name}' for review.",
        task,
    )
    return JsonResponse(
        {
            "id": submission.id,
            "task_id": task.id,
            "description": submission.description,
            "submitted_at": submission.submitted_at,
            "review_status": submission.review_status,
        },
        status=201,
    )


def review_task_submission(request, task_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    task, error = _require_task_access(request, task_id)
    if error:
        return error
    _, error = _require_team_access(request, task.team_id, leader=True)
    if error:
        return error
    data, error = _read_json_body(request)
    if error:
        return error
    submission_id = data.get("submission_id")
    review_status = data.get("review_status")
    if review_status not in ("approved", "rejected"):
        return JsonResponse(
            {"error": "review_status must be 'approved' or 'rejected'"},
            status=400,
        )
    if not _is_positive_integer(submission_id):
        return JsonResponse({"error": "submission_id must be a submission ID"}, status=400)
    submission = TaskSubmission.objects.filter(
        id=submission_id,
        task=task,
        review_status="pending",
    ).first()
    if submission is None:
        return JsonResponse({"error": "Pending submission not found"}, status=404)
    feedback = data.get("feedback", "")
    if not isinstance(feedback, str):
        return JsonResponse({"error": "feedback must be a string"}, status=400)
    submission.review_status = review_status
    submission.feedback = feedback
    submission.save(update_fields=["review_status", "feedback"])
    if review_status == "rejected":
        task.status = "inprogress"
        task.completed_at = None
        task.save(update_fields=["status", "completed_at"])
    _record_activity(
        task.team,
        request.user,
        "task_submission_reviewed",
        f"{request.user.username} {review_status} submission for '{task.task_name}'.",
        task,
    )
    return JsonResponse(
        {
            "id": submission.id,
            "review_status": submission.review_status,
            "feedback": submission.feedback,
        }
    )


def team_assigned_tasks(request, team_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    team, error = _require_team_access(request, team_id, leader=True)
    if error:
        return error
    tasks = Task.objects.filter(
        team=team,
        created_by=request.user,
    ).select_related("team", "assigned_to", "created_by").order_by(
        "deadline", "id"
    )
    return JsonResponse({"tasks": [_task_json(task) for task in tasks]})


def task_comments(request, task_id):
    if request.method not in ("GET", "POST"):
        return JsonResponse({"error": "Method not allowed"}, status=405)
    task, error = _require_task_access(request, task_id)
    if error:
        return error
    if request.method == "GET":
        comments = task.comments.select_related("user").order_by("created_at")
        return JsonResponse({
            "comments": [
                {
                    "id": comment.id,
                    "user_id": comment.user_id,
                    "username": comment.user.username if comment.user else None,
                    "content": comment.content,
                    "created_at": comment.created_at,
                }
                for comment in comments
            ]
        })
    data, error = _read_json_body(request)
    if error:
        return error
    content = data.get("content")
    if not isinstance(content, str) or not content.strip():
        return JsonResponse({"error": "content is required"}, status=400)
    comment = Comment.objects.create(
        task=task,
        user=request.user,
        content=content.strip(),
    )
    _record_activity(
        task.team,
        request.user,
        "comment_added",
        f"{request.user.username} commented on '{task.task_name}'.",
        task,
    )
    return JsonResponse(
        {
            "id": comment.id,
            "user_id": comment.user_id,
            "username": request.user.username,
            "content": comment.content,
            "created_at": comment.created_at,
        },
        status=201,
    )


def task_attachments(request, task_id):
    if request.method not in ("GET", "POST"):
        return JsonResponse({"error": "Method not allowed"}, status=405)
    task, error = _require_task_access(request, task_id)
    if error:
        return error
    if request.method == "GET":
        attachments = task.attachments.select_related("uploaded_by").order_by(
            "uploaded_at"
        )
        return JsonResponse({
            "attachments": [
                {
                    "id": attachment.id,
                    "uploaded_by": attachment.uploaded_by_id,
                    "username": (
                        attachment.uploaded_by.username
                        if attachment.uploaded_by else None
                    ),
                    "file_name": attachment.file.name,
                    "url": attachment.file.url,
                    "uploaded_at": attachment.uploaded_at,
                }
                for attachment in attachments
            ]
        })
    uploaded_file = request.FILES.get("file")
    if uploaded_file is None:
        return JsonResponse({"error": "file is required"}, status=400)
    attachment = Attachment.objects.create(
        task=task,
        uploaded_by=request.user,
        file=uploaded_file,
    )
    _record_activity(
        task.team,
        request.user,
        "attachment_uploaded",
        f"{request.user.username} uploaded an attachment to '{task.task_name}'.",
        task,
    )
    return JsonResponse(
        {
            "id": attachment.id,
            "file_name": attachment.file.name,
            "url": attachment.file.url,
            "uploaded_at": attachment.uploaded_at,
        },
        status=201,
    )


def delete_attachment(request, attachment_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)
    attachment = Attachment.objects.select_related("task__team").filter(
        id=attachment_id
    ).first()
    if attachment is None:
        return JsonResponse({"error": "Attachment not found"}, status=404)
    _, error = _require_team_access(request, attachment.task.team_id)
    if error:
        return error
    is_leader = Membership.objects.filter(
        user=request.user,
        team=attachment.task.team,
        status="approved",
        role__iexact="leader",
    ).exists()
    if attachment.uploaded_by_id != request.user.id and not is_leader:
        return JsonResponse({"error": "Only the uploader or team leader may delete it"}, status=403)
    attachment.delete()
    return JsonResponse({"message": "Attachment deleted"})


def user_notifications(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    return JsonResponse({
        "notifications": [
            {
                "id": notification.id,
                "team_id": notification.team_id,
                "title": notification.title,
                "message": notification.message,
                "is_read": notification.is_read,
                "created_at": notification.created_at,
            }
            for notification in notifications
        ]
    })


def mark_notification_read(request, notification_id=None):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)
    notifications = Notification.objects.filter(user=request.user)
    if notification_id is None:
        updated_count = notifications.filter(is_read=False).update(is_read=True)
        return JsonResponse({"message": "Notifications marked as read", "updated": updated_count})
    notification = notifications.filter(id=notification_id).first()
    if notification is None:
        return JsonResponse({"error": "Notification not found"}, status=404)
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])
    return JsonResponse({"message": "Notification marked as read"})


def delete_notification(request, notification_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)
    notification = Notification.objects.filter(
        id=notification_id,
        user=request.user,
    ).first()
    if notification is None:
        return JsonResponse({"error": "Notification not found"}, status=404)
    notification.delete()
    return JsonResponse({"message": "Notification deleted"})


def team_meetings(request, team_id):
    if request.method not in ("GET", "POST"):
        return JsonResponse({"error": "Method not allowed"}, status=405)
    team, error = _require_team_access(
        request,
        team_id,
        leader=request.method == "POST",
    )
    if error:
        return error
    if request.method == "GET":
        meetings = Meeting.objects.filter(team=team).order_by("scheduled_at", "id")
        return JsonResponse({"meetings": [_meeting_json(meeting) for meeting in meetings]})

    data, error = _read_json_body(request)
    if error:
        return error
    title = data.get("title")
    description = data.get("description", "")
    meeting_link = data.get("meeting_link")
    if not isinstance(title, str) or not title.strip():
        return JsonResponse({"error": "title is required"}, status=400)
    if not isinstance(description, str):
        return JsonResponse({"error": "description must be a string"}, status=400)
    if meeting_link is not None and not isinstance(meeting_link, str):
        return JsonResponse({"error": "meeting_link must be a string or null"}, status=400)
    scheduled_at, error = _parse_datetime_field(
        data.get("scheduled_at"),
        "scheduled_at",
    )
    if error:
        return error
    meeting = Meeting.objects.create(
        team=team,
        title=title.strip(),
        description=description,
        scheduled_at=scheduled_at,
        meeting_link=meeting_link or None,
        created_by=request.user,
    )
    _record_activity(
        team,
        request.user,
        "meeting_scheduled",
        f"{request.user.username} scheduled '{meeting.title}'.",
    )
    return JsonResponse(_meeting_json(meeting), status=201)


def meeting_detail(request, meeting_id):
    if request.method not in ("GET", "PUT", "DELETE"):
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)
    meeting = Meeting.objects.select_related("team").filter(id=meeting_id).first()
    if meeting is None:
        return JsonResponse({"error": "Meeting not found"}, status=404)
    _, error = _require_team_access(
        request,
        meeting.team_id,
        leader=request.method in ("PUT", "DELETE"),
    )
    if error:
        return error
    if request.method == "GET":
        return JsonResponse(_meeting_json(meeting))
    if request.method == "DELETE":
        meeting.status = "cancelled"
        meeting.save(update_fields=["status", "updated_at"])
        _record_activity(
            meeting.team,
            request.user,
            "meeting_cancelled",
            f"{request.user.username} cancelled '{meeting.title}'.",
        )
        return JsonResponse({"message": "Meeting cancelled"})

    data, error = _read_json_body(request)
    if error:
        return error
    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return JsonResponse({"error": "title cannot be empty"}, status=400)
        meeting.title = data["title"].strip()
    if "description" in data:
        if not isinstance(data["description"], str):
            return JsonResponse({"error": "description must be a string"}, status=400)
        meeting.description = data["description"]
    if "scheduled_at" in data:
        meeting.scheduled_at, error = _parse_datetime_field(
            data["scheduled_at"],
            "scheduled_at",
        )
        if error:
            return error
    if "meeting_link" in data:
        meeting_link = data["meeting_link"]
        if meeting_link is not None and not isinstance(meeting_link, str):
            return JsonResponse(
                {"error": "meeting_link must be a string or null"},
                status=400,
            )
        meeting.meeting_link = meeting_link or None
    if "status" in data:
        if data["status"] not in dict(Meeting.STATUS_CHOICES):
            return JsonResponse({"error": "Invalid meeting status"}, status=400)
        meeting.status = data["status"]
    meeting.save()
    _record_activity(
        meeting.team,
        request.user,
        "meeting_updated",
        f"{request.user.username} updated '{meeting.title}'.",
    )
    return JsonResponse(_meeting_json(meeting))