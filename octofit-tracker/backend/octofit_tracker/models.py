from djongo import models
from django.utils import timezone


class Team(models.Model):
    _id = models.CharField(max_length=100, primary_key=True, db_column='_id')
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    member_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column='_id')
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    hero_name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=100)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.name} ({self.hero_name})"


class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column='_id')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    calories_per_session = models.IntegerField()
    description = models.TextField()
    difficulty = models.CharField(max_length=50)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column='_id')
    user_id = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=200)
    hero_name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    workout_name = models.CharField(max_length=200)
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField()
    points = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']

    def __str__(self):
        return f"{self.hero_name} - {self.activity_type} ({self.date.strftime('%Y-%m-%d')})"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column='_id')
    leaderboard_type = models.CharField(max_length=50)  # 'individual' or 'team'
    rank = models.IntegerField()
    total_points = models.IntegerField()
    last_updated = models.DateTimeField(default=timezone.now)
    
    # For individual leaderboard
    user_id = models.CharField(max_length=100, null=True, blank=True)
    user_email = models.EmailField(null=True, blank=True)
    user_name = models.CharField(max_length=200, null=True, blank=True)
    hero_name = models.CharField(max_length=200, null=True, blank=True)
    team_id = models.CharField(max_length=100, null=True, blank=True)
    
    # For team leaderboard
    team_name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['leaderboard_type', 'rank']

    def __str__(self):
        if self.leaderboard_type == 'individual':
            return f"#{self.rank} {self.hero_name} - {self.total_points} pts"
        else:
            return f"#{self.rank} {self.team_name} - {self.total_points} pts"
