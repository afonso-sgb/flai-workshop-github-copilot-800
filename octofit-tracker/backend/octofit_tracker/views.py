from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer, 
    LeaderboardSerializer, WorkoutSerializer
)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'member_count', 'created_at']
    ordering = ['name']


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['team_id', 'email']
    search_fields = ['name', 'hero_name', 'email']
    ordering_fields = ['name', 'total_points', 'created_at']
    ordering = ['-total_points']

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get users grouped by team"""
        team_id = request.query_params.get('team_id', None)
        if team_id:
            users = User.objects.filter(team_id=team_id)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response({'error': 'team_id parameter is required'}, status=400)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workouts
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'difficulty']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'duration_minutes', 'calories_per_session', 'difficulty']
    ordering = ['name']


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_id', 'team_id', 'activity_type']
    search_fields = ['user_name', 'hero_name', 'workout_name']
    ordering_fields = ['date', 'points', 'calories_burned', 'duration_minutes']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities for a specific user"""
        user_id = request.query_params.get('user_id', None)
        if user_id:
            activities = Activity.objects.filter(user_id=user_id)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'user_id parameter is required'}, status=400)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get activities for a specific team"""
        team_id = request.query_params.get('team_id', None)
        if team_id:
            activities = Activity.objects.filter(team_id=team_id)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'team_id parameter is required'}, status=400)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for leaderboard (read-only)
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['leaderboard_type', 'team_id']
    ordering_fields = ['rank', 'total_points']
    ordering = ['rank']

    @action(detail=False, methods=['get'])
    def individual(self, request):
        """Get individual leaderboard"""
        leaderboard = Leaderboard.objects.filter(leaderboard_type='individual').order_by('rank')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def team(self, request):
        """Get team leaderboard"""
        leaderboard = Leaderboard.objects.filter(leaderboard_type='team').order_by('rank')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
