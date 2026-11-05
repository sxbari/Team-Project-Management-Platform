from django.test import TestCase
from .models import Team

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