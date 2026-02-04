from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['_id', 'name', 'member_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'hero_name', 'email', 'team_id', 'total_points', 'created_at']
    search_fields = ['name', 'hero_name', 'email']
    list_filter = ['team_id', 'created_at']
    ordering = ['-total_points']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'duration_minutes', 'calories_per_session', 'difficulty']
    search_fields = ['name', 'description']
    list_filter = ['type', 'difficulty']
    ordering = ['name']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['hero_name', 'activity_type', 'workout_name', 'duration_minutes', 
                    'calories_burned', 'points', 'date', 'team_id']
    search_fields = ['user_name', 'hero_name', 'workout_name']
    list_filter = ['activity_type', 'team_id', 'date']
    ordering = ['-date']
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['rank', 'leaderboard_type', 'get_display_name', 'total_points', 'last_updated']
    search_fields = ['hero_name', 'team_name', 'user_name']
    list_filter = ['leaderboard_type', 'last_updated']
    ordering = ['leaderboard_type', 'rank']

    def get_display_name(self, obj):
        if obj.leaderboard_type == 'individual':
            return f"{obj.hero_name} ({obj.user_name})"
        else:
            return obj.team_name
    get_display_name.short_description = 'Name'
