from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at', 'member_count']


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
    class Meta:
        model = Leaderboard
        fields = ['_id', 'leaderboard_type', 'rank', 'total_points', 'last_updated',
                  'user_id', 'user_email', 'user_name', 'hero_name', 'team_id', 'team_name']
