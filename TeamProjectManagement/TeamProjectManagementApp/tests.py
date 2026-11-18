from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from .models import Team


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