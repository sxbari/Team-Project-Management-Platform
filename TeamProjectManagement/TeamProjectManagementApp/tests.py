import json
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from .models import Meeting, Membership, Notification, Task, Team, TaskSubmission


class UrlRoutingTests(SimpleTestCase):

    def test_existing_team_membership_and_task_views_have_descriptive_handlers(self):
        self.assertEqual(resolve(reverse("teams")).func.__name__, "team_list_create")
        self.assertEqual(
            resolve(reverse("membership", args=[1])).func.__name__,
            "team_membership_list_create",
        )
        self.assertEqual(
            resolve(reverse("tasks")).func.__name__,
            "assigned_tasks_list_create",
        )

    def test_remaining_views_have_routes(self):
        routes = {
            "logout": ("logout/", {}),
            "my_requests": ("my-requests/", {}),
            "send_request": ("send-request/", {}),
            "team_detail": ("teams/1/", {"team_id": 1}),
            "team_members": ("teams/1/members/", {"team_id": 1}),
            "member_leave": ("teams/1/leave/", {"team_id": 1}),
            "team_activity": ("teams/1/activity/", {"team_id": 1}),
            "team_join_requests": ("teams/1/join-requests/", {"team_id": 1}),
            "approve_join_request": ("memberships/1/approve/", {"membership_id": 1}),
            "reject_join_request": ("memberships/1/reject/", {"membership_id": 1}),
            "remove_team_member": (
                "teams/1/remove-member/2/",
                {"team_id": 1, "membership_id": 2},
            ),
            "my_tasks": ("my-tasks/", {}),
            "task_history": ("task-history/", {}),
            "team_tasks": ("teams/1/tasks/", {"team_id": 1}),
            "create_team_task": ("teams/1/create-task/", {"team_id": 1}),
            "task_detail": ("tasks/1/", {"task_id": 1}),
            "update_task": ("tasks/1/update/", {"task_id": 1}),
            "assign_task": ("tasks/1/assign/", {"task_id": 1}),
            "update_task_status": ("tasks/1/update-status/", {"task_id": 1}),
            "submit_task": ("tasks/1/submit/", {"task_id": 1}),
            "review_task_submission": ("tasks/1/review/", {"task_id": 1}),
            "team_assigned_tasks": ("teams/1/assigned-tasks/", {"team_id": 1}),
            "task_comments": ("tasks/1/comments/", {"task_id": 1}),
            "task_attachments": ("tasks/1/attachments/", {"task_id": 1}),
            "delete_attachment": ("attachments/1/", {"attachment_id": 1}),
            "notifications": ("notifications/", {}),
            "notification_read": ("notifications/1/read/", {"notification_id": 1}),
            "notifications_read_all": ("notifications/read-all/", {}),
            "notification_delete": ("notifications/1/", {"notification_id": 1}),
            "team_meetings": ("teams/1/meetings/", {"team_id": 1}),
            "meeting_detail": ("meetings/1/", {"meeting_id": 1}),
        }

        for route_name, (expected_path, kwargs) in routes.items():
            with self.subTest(route_name=route_name):
                self.assertEqual(reverse(route_name, kwargs=kwargs), f"/api/{expected_path}")


class TeamTests(TestCase):

    def test_get_teams(self):
        Team.objects.create(
            team_name="Backend Team",
            description="Django development"
        )
        Team.objects.create(
                team_name="Frontend Team",
                description="React development"
        )

        response = self.client.get("/api/teams/")

        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(len(response.json()), 2)


class TeamWorkflowTests(TestCase):

    def setUp(self):
        self.leader = User.objects.create_user(username="leader", password="pass")
        self.member = User.objects.create_user(username="member", password="pass")
        self.client.force_login(self.leader)
        response = self.client.post(
            "/api/teams/",
            data=json.dumps({
                "team_name": "Platform",
                "description": "Platform team",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.team = Team.objects.get(team_name="Platform")
        self.member_membership = Membership.objects.create(
            user=self.member,
            team=self.team,
            role="member",
            status="approved",
        )

    def test_leader_task_submission_and_review_flow(self):
        task_response = self.client.post(
            reverse("create_team_task", args=[self.team.id]),
            data=json.dumps({
                "task_name": "Build API",
                "description": "Implement the API",
                "deadline": "2027-01-01T10:00:00Z",
                "assigned_to": self.member.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(task_response.status_code, 201, task_response.content)
        task = Task.objects.get(task_name="Build API")
        self.assertEqual(task.created_by, self.leader)

        self.client.force_login(self.member)
        comment_response = self.client.post(
            reverse("task_comments", args=[task.id]),
            data=json.dumps({"content": "Starting now"}),
            content_type="application/json",
        )
        self.assertEqual(comment_response.status_code, 201)
        self.assertEqual(
            self.client.get(reverse("my_tasks")).json()["tasks"][0]["id"],
            task.id,
        )
        submit_response = self.client.post(
            reverse("submit_task", args=[task.id]),
            data=json.dumps({"description": "Work is complete"}),
            content_type="application/json",
        )
        self.assertEqual(submit_response.status_code, 201, submit_response.content)
        submission = TaskSubmission.objects.get(task=task)
        task.refresh_from_db()
        self.assertEqual(task.status, "completed")

        self.client.force_login(self.leader)
        review_response = self.client.post(
            reverse("review_task_submission", args=[task.id]),
            data=json.dumps({
                "submission_id": submission.id,
                "review_status": "approved",
                "feedback": "Looks good",
            }),
            content_type="application/json",
        )
        self.assertEqual(review_response.status_code, 200, review_response.content)
        submission.refresh_from_db()
        self.assertEqual(submission.review_status, "approved")

    def test_meeting_notification_and_join_request_endpoints(self):
        pending = Membership.objects.create(
            user=User.objects.create_user(username="applicant", password="pass"),
            team=self.team,
            role="member",
            status="pending",
        )
        requests_response = self.client.get(
            reverse("team_join_requests", args=[self.team.id])
        )
        self.assertEqual(requests_response.status_code, 200)
        self.assertEqual(requests_response.json()["requests"][0]["id"], pending.id)
        approve_response = self.client.post(
            reverse("approve_join_request", args=[pending.id])
        )
        self.assertEqual(approve_response.status_code, 200)

        meeting_response = self.client.post(
            reverse("team_meetings", args=[self.team.id]),
            data=json.dumps({
                "title": "Planning",
                "scheduled_at": "2027-01-02T10:00:00Z",
            }),
            content_type="application/json",
        )
        self.assertEqual(meeting_response.status_code, 201, meeting_response.content)
        meeting = Meeting.objects.get(title="Planning")
        update_response = self.client.put(
            reverse("meeting_detail", args=[meeting.id]),
            data=json.dumps({"status": "completed"}),
            content_type="application/json",
        )
        self.assertEqual(update_response.status_code, 200)
        delete_response = self.client.delete(
            reverse("meeting_detail", args=[meeting.id])
        )
        self.assertEqual(delete_response.status_code, 200)
        meeting.refresh_from_db()
        self.assertEqual(meeting.status, "cancelled")

        Notification.objects.create(
            user=self.leader,
            team=self.team,
            title="Update",
            message="A notification",
        )
        notification = self.client.get(reverse("notifications")).json()["notifications"][0]
        read_response = self.client.post(
            reverse("notification_read", args=[notification["id"]])
        )
        self.assertEqual(read_response.status_code, 200)
        self.assertTrue(Notification.objects.get(id=notification["id"]).is_read)