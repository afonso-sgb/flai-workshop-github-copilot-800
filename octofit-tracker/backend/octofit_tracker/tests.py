from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from .models import User, Team, Activity, Leaderboard, Workout


class TeamModelTestCase(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            _id='test_team',
            name='Test Team',
            description='A test team',
            member_count=5
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.member_count, 5)
        self.assertEqual(str(self.team), 'Test Team')


class UserModelTestCase(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test Hero',
            email='test@hero.com',
            hero_name='The Tester',
            team_id='test_team',
            total_points=100
        )
    
    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.name, 'Test Hero')
        self.assertEqual(self.user.email, 'test@hero.com')
        self.assertEqual(self.user.hero_name, 'The Tester')
        self.assertEqual(str(self.user), 'Test Hero (The Tester)')


class WorkoutModelTestCase(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Test Workout',
            type='cardio',
            duration_minutes=30,
            calories_per_session=300,
            description='A test workout',
            difficulty='intermediate'
        )
    
    def test_workout_creation(self):
        """Test that a workout can be created"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.duration_minutes, 30)
        self.assertEqual(str(self.workout), 'Test Workout')


class TeamAPITestCase(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            _id='test_team',
            name='Test Team',
            description='A test team',
            member_count=5
        )
    
    def test_get_teams_list(self):
        """Test retrieving teams list"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_team_detail(self):
        """Test retrieving a single team"""
        url = reverse('team-detail', kwargs={'pk': 'test_team'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Team')


class UserAPITestCase(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Test Hero',
            email='test@hero.com',
            hero_name='The Tester',
            team_id='test_team',
            total_points=100
        )
    
    def test_get_users_list(self):
        """Test retrieving users list"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class WorkoutAPITestCase(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='Test Workout',
            type='cardio',
            duration_minutes=30,
            calories_per_session=300,
            description='A test workout',
            difficulty='intermediate'
        )
    
    def test_get_workouts_list(self):
        """Test retrieving workouts list"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ActivityAPITestCase(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.activity = Activity.objects.create(
            user_id='test_user_id',
            user_email='test@hero.com',
            user_name='Test Hero',
            hero_name='The Tester',
            team_id='test_team',
            activity_type='running',
            workout_name='Test Workout',
            duration_minutes=30,
            calories_burned=300,
            points=50,
            date=timezone.now(),
            notes='Test activity'
        )
    
    def test_get_activities_list(self):
        """Test retrieving activities list"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class LeaderboardAPITestCase(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.leaderboard_entry = Leaderboard.objects.create(
            leaderboard_type='individual',
            rank=1,
            total_points=500,
            user_id='test_user_id',
            user_email='test@hero.com',
            user_name='Test Hero',
            hero_name='The Tester',
            team_id='test_team'
        )
    
    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard list"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_individual_leaderboard(self):
        """Test retrieving individual leaderboard"""
        url = reverse('leaderboard-individual')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class APIRootTestCase(APITestCase):
    """Test cases for API root endpoint"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_api_root(self):
        """Test that API root returns all endpoints"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('teams', response.data)
        self.assertIn('users', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('workouts', response.data)
        self.assertIn('leaderboard', response.data)
