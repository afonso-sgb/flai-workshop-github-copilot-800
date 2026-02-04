from rest_framework import serializers
from django.db import models as django_models
from .models import User, Team, Activity, Leaderboard, Workout


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at', 'member_count', 'members']
    
    def get_members(self, obj):
        """Get list of users belonging to this team"""
        users = User.objects.filter(team_id=obj._id)
        return [{'name': user.name, 'hero_name': user.hero_name, 'email': user.email} for user in users]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'hero_name', 'team_id', 'total_points', 'created_at']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'type', 'duration_minutes', 'calories_per_session', 'description', 'difficulty']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['_id', 'user_id', 'user_email', 'user_name', 'hero_name', 'team_id', 
                  'activity_type', 'workout_name', 'duration_minutes', 'calories_burned', 
                  'points', 'date', 'notes']


class LeaderboardSerializer(serializers.ModelSerializer):
    team_name_display = serializers.SerializerMethodField()
    total_calories = serializers.SerializerMethodField()
    activity_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['_id', 'leaderboard_type', 'rank', 'total_points', 'last_updated',
                  'user_id', 'user_email', 'user_name', 'hero_name', 'team_id', 'team_name',
                  'team_name_display', 'total_calories', 'activity_count']
    
    def get_team_name_display(self, obj):
        """Get the team name for individual leaderboard entries"""
        if obj.leaderboard_type == 'individual' and obj.team_id:
            try:
                team = Team.objects.get(_id=obj.team_id)
                return team.name
            except Team.DoesNotExist:
                return None
        return obj.team_name
    
    def get_total_calories(self, obj):
        """Calculate total calories burned by this user"""
        if obj.leaderboard_type == 'individual' and obj.user_id:
            total = Activity.objects.filter(user_id=obj.user_id).aggregate(
                total=django_models.Sum('calories_burned')
            )['total']
            return total or 0
        return 0
    
    def get_activity_count(self, obj):
        """Count total activities for this user"""
        if obj.leaderboard_type == 'individual' and obj.user_id:
            return Activity.objects.filter(user_id=obj.user_id).count()
        return 0
