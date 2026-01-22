from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="testpass123",
            team="Team A"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.team, "Team A")


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name="Team A",
            description="Test team description"
        )

    def test_team_creation(self):
        self.assertEqual(self.team.name, "Team A")
        self.assertEqual(self.team.description, "Test team description")


class ActivityModelTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email="test@example.com",
            activity_type="Running",
            duration=30,
            calories=300,
            date=datetime.now()
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.user_email, "test@example.com")
        self.assertEqual(self.activity.activity_type, "Running")
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories, 300)


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.entry = Leaderboard.objects.create(
            user_email="test@example.com",
            user_name="Test User",
            team="Team A",
            total_calories=1000,
            total_activities=5,
            rank=1
        )

    def test_leaderboard_creation(self):
        self.assertEqual(self.entry.user_name, "Test User")
        self.assertEqual(self.entry.total_calories, 1000)
        self.assertEqual(self.entry.rank, 1)


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            name="Morning Run",
            description="A refreshing morning run",
            difficulty="Medium",
            duration=45,
            target_calories=400,
            exercises=["Running", "Warm-up", "Cool-down"]
        )

    def test_workout_creation(self):
        self.assertEqual(self.workout.name, "Morning Run")
        self.assertEqual(self.workout.difficulty, "Medium")
        self.assertEqual(self.workout.duration, 45)


class UserAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "name": "API Test User",
            "email": "apitest@example.com",
            "password": "testpass123",
            "team": "Team B"
        }

    def test_create_user(self):
        response = self.client.post('/api/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users(self):
        User.objects.create(**self.user_data)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            "name": "API Test Team",
            "description": "Test team for API testing"
        }

    def test_create_team(self):
        response = self.client.post('/api/teams/', self.team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_teams(self):
        Team.objects.create(**self.team_data)
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
