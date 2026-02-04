from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        
        self.stdout.write(self.style.SUCCESS('Connected to MongoDB'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})
        
        # Create unique index on email field for users collection
        db.users.create_index([("email", 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))
        
        # Insert Teams
        teams_data = [
            {
                '_id': 'team_marvel',
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'created_at': datetime.now(),
                'member_count': 0
            },
            {
                '_id': 'team_dc',
                'name': 'Team DC',
                'description': 'Justice League United',
                'created_at': datetime.now(),
                'member_count': 0
            }
        ]
        db.teams.insert_many(teams_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(teams_data)} teams'))
        
        # Insert Users (Superheroes)
        users_data = [
            # Team Marvel
            {
                'name': 'Tony Stark',
                'email': 'ironman@marvel.com',
                'hero_name': 'Iron Man',
                'team_id': 'team_marvel',
                'total_points': 0,
                'created_at': datetime.now()
            },
            {
                'name': 'Steve Rogers',
                'email': 'captainamerica@marvel.com',
                'hero_name': 'Captain America',
                'team_id': 'team_marvel',
                'total_points': 0,
                'created_at': datetime.now()
            },
            {
                'name': 'Natasha Romanoff',
                'email': 'blackwidow@marvel.com',
                'hero_name': 'Black Widow',
                'team_id': 'team_marvel',
                'total_points': 0,
                'created_at': datetime.now()
            },
            {
                'name': 'Bruce Banner',
                'email': 'hulk@marvel.com',
                'hero_name': 'Hulk',
                'team_id': 'team_marvel',
                'total_points': 0,
                'created_at': datetime.now()
            },
            {
                'name': 'Thor Odinson',
                'email': 'thor@marvel.com',
                'hero_name': 'Thor',
                'team_id': 'team_marvel',
                'total_points': 0,
                'created_at': datetime.now()
            },
            # Team DC
            {
                'name': 'Clark Kent',
                'email': 'superman@dc.com',
                'hero_name': 'Superman',
                'team_id': 'team_dc',
                'total_points': 0,
                'created_at': datetime.now()
            },
            {
                'name': 'Bruce Wayne',
                'email': 'batman@dc.com',
                'hero_name': 'Batman',
                'team_id': 'team_dc',
                'total_points': 0,
                'created_at': datetime.now()
            },
            {
                'name': 'Diana Prince',
                'email': 'wonderwoman@dc.com',
                'hero_name': 'Wonder Woman',
                'team_id': 'team_dc',
                'total_points': 0,
                'created_at': datetime.now()
            },
            {
                'name': 'Barry Allen',
                'email': 'flash@dc.com',
                'hero_name': 'Flash',
                'team_id': 'team_dc',
                'total_points': 0,
                'created_at': datetime.now()
            },
            {
                'name': 'Arthur Curry',
                'email': 'aquaman@dc.com',
                'hero_name': 'Aquaman',
                'team_id': 'team_dc',
                'total_points': 0,
                'created_at': datetime.now()
            }
        ]
        result = db.users.insert_many(users_data)
        user_ids = result.inserted_ids
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(users_data)} users'))
        
        # Update team member counts
        db.teams.update_one({'_id': 'team_marvel'}, {'$set': {'member_count': 5}})
        db.teams.update_one({'_id': 'team_dc'}, {'$set': {'member_count': 5}})
        
        # Insert Workouts
        workouts_data = [
            {
                'name': 'Super Strength Training',
                'type': 'strength',
                'duration_minutes': 45,
                'calories_per_session': 400,
                'description': 'Build strength like a superhero',
                'difficulty': 'advanced'
            },
            {
                'name': 'Speed Force Cardio',
                'type': 'cardio',
                'duration_minutes': 30,
                'calories_per_session': 350,
                'description': 'Run at lightning speed',
                'difficulty': 'intermediate'
            },
            {
                'name': 'Avenger Yoga',
                'type': 'flexibility',
                'duration_minutes': 60,
                'calories_per_session': 200,
                'description': 'Find your inner peace',
                'difficulty': 'beginner'
            },
            {
                'name': 'Justice League HIIT',
                'type': 'hiit',
                'duration_minutes': 25,
                'calories_per_session': 450,
                'description': 'High intensity heroic training',
                'difficulty': 'advanced'
            },
            {
                'name': 'Web-Slinging Workout',
                'type': 'mixed',
                'duration_minutes': 40,
                'calories_per_session': 380,
                'description': 'Full body workout',
                'difficulty': 'intermediate'
            },
            {
                'name': 'Asgardian Battle Training',
                'type': 'strength',
                'duration_minutes': 50,
                'calories_per_session': 420,
                'description': 'Train like a god',
                'difficulty': 'advanced'
            }
        ]
        result = db.workouts.insert_many(workouts_data)
        workout_ids = result.inserted_ids
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workouts_data)} workouts'))
        
        # Insert Activities (last 30 days)
        activities_data = []
        activity_types = ['running', 'cycling', 'swimming', 'weightlifting', 'yoga', 'hiit']
        
        for user_id, user in zip(user_ids, users_data):
            # Each user has 10-20 activities
            num_activities = random.randint(10, 20)
            for i in range(num_activities):
                days_ago = random.randint(0, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
                
                workout = random.choice(workouts_data)
                duration = workout['duration_minutes'] + random.randint(-10, 10)
                calories = workout['calories_per_session'] + random.randint(-50, 50)
                points = int(calories / 10) + random.randint(0, 20)
                
                activity = {
                    'user_id': user_id,
                    'user_email': user['email'],
                    'user_name': user['name'],
                    'hero_name': user['hero_name'],
                    'team_id': user['team_id'],
                    'activity_type': random.choice(activity_types),
                    'workout_name': workout['name'],
                    'duration_minutes': duration,
                    'calories_burned': calories,
                    'points': points,
                    'date': activity_date,
                    'notes': f'{user["hero_name"]} saving the world one workout at a time!'
                }
                activities_data.append(activity)
        
        db.activities.insert_many(activities_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(activities_data)} activities'))
        
        # Calculate and update user total points
        for user_id, user in zip(user_ids, users_data):
            user_activities = [a for a in activities_data if a['user_id'] == user_id]
            total_points = sum(a['points'] for a in user_activities)
            db.users.update_one({'_id': user_id}, {'$set': {'total_points': total_points}})
        
        self.stdout.write(self.style.SUCCESS('Updated user total points'))
        
        # Insert Leaderboard entries
        leaderboard_data = []
        
        # Individual leaderboard
        users_with_points = []
        for user_id, user in zip(user_ids, users_data):
            user_activities = [a for a in activities_data if a['user_id'] == user_id]
            total_points = sum(a['points'] for a in user_activities)
            users_with_points.append({
                'user_id': user_id,
                'user_email': user['email'],
                'user_name': user['name'],
                'hero_name': user['hero_name'],
                'team_id': user['team_id'],
                'total_points': total_points
            })
        
        users_with_points.sort(key=lambda x: x['total_points'], reverse=True)
        
        for rank, user_data in enumerate(users_with_points, 1):
            leaderboard_entry = {
                'user_id': user_data['user_id'],
                'user_email': user_data['user_email'],
                'user_name': user_data['user_name'],
                'hero_name': user_data['hero_name'],
                'team_id': user_data['team_id'],
                'total_points': user_data['total_points'],
                'rank': rank,
                'leaderboard_type': 'individual',
                'last_updated': datetime.now()
            }
            leaderboard_data.append(leaderboard_entry)
        
        # Team leaderboard
        team_points = {}
        for team_data in teams_data:
            team_id = team_data['_id']
            team_activities = [a for a in activities_data if a['team_id'] == team_id]
            total_points = sum(a['points'] for a in team_activities)
            team_points[team_id] = {
                'team_id': team_id,
                'team_name': team_data['name'],
                'total_points': total_points
            }
        
        sorted_teams = sorted(team_points.values(), key=lambda x: x['total_points'], reverse=True)
        
        for rank, team_data in enumerate(sorted_teams, 1):
            leaderboard_entry = {
                'team_id': team_data['team_id'],
                'team_name': team_data['team_name'],
                'total_points': team_data['total_points'],
                'rank': rank,
                'leaderboard_type': 'team',
                'last_updated': datetime.now()
            }
            leaderboard_data.append(leaderboard_entry)
        
        db.leaderboard.insert_many(leaderboard_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(leaderboard_data)} leaderboard entries'))
        
        # Display summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Users: {db.users.count_documents({})}')
        self.stdout.write(f'Teams: {db.teams.count_documents({})}')
        self.stdout.write(f'Activities: {db.activities.count_documents({})}')
        self.stdout.write(f'Workouts: {db.workouts.count_documents({})}')
        self.stdout.write(f'Leaderboard entries: {db.leaderboard.count_documents({})}')
        
        client.close()
        self.stdout.write(self.style.SUCCESS('\nDatabase populated successfully!'))
