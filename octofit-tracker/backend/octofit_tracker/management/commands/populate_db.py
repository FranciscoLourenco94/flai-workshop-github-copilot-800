from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write('Creating teams...')
        
        # Create teams
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='The mightiest heroes of Earth'
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League defenders'
        )

        self.stdout.write('Creating users...')
        
        # Marvel superheroes
        marvel_users = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com', 'password': 'jarvis123', 'team': 'Team Marvel'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com', 'password': 'shield456', 'team': 'Team Marvel'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com', 'password': 'asgard789', 'team': 'Team Marvel'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'password': 'redroom101', 'team': 'Team Marvel'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com', 'password': 'gamma112', 'team': 'Team Marvel'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com', 'password': 'webslinger131', 'team': 'Team Marvel'},
        ]
        
        # DC superheroes
        dc_users = [
            {'name': 'Superman', 'email': 'clark.kent@dc.com', 'password': 'krypton123', 'team': 'Team DC'},
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com', 'password': 'gotham456', 'team': 'Team DC'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com', 'password': 'themyscira789', 'team': 'Team DC'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com', 'password': 'speedforce101', 'team': 'Team DC'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com', 'password': 'atlantis112', 'team': 'Team DC'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com', 'password': 'willpower131', 'team': 'Team DC'},
        ]
        
        all_users = []
        for user_data in marvel_users + dc_users:
            user = User.objects.create(**user_data)
            all_users.append(user)

        self.stdout.write('Creating activities...')
        
        # Activity types with calorie ranges
        activity_types = {
            'Running': (400, 800),
            'Cycling': (300, 700),
            'Swimming': (350, 750),
            'Weight Training': (250, 500),
            'Boxing': (450, 850),
            'Yoga': (150, 300),
            'HIIT': (500, 900),
            'Martial Arts': (400, 800),
        }
        
        # Create activities for the past 30 days
        for user in all_users:
            num_activities = random.randint(5, 15)
            for _ in range(num_activities):
                activity_type = random.choice(list(activity_types.keys()))
                min_cal, max_cal = activity_types[activity_type]
                
                duration = random.randint(20, 120)
                calories = random.randint(min_cal, max_cal)
                days_ago = random.randint(0, 30)
                activity_date = timezone.now() - timedelta(days=days_ago)
                
                Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type,
                    duration=duration,
                    calories=calories,
                    date=activity_date
                )

        self.stdout.write('Creating leaderboard...')
        
        # Create leaderboard entries
        for user in all_users:
            activities = Activity.objects.filter(user_email=user.email)
            total_calories = sum(activity.calories for activity in activities)
            total_activities = activities.count()
            
            Leaderboard.objects.create(
                user_email=user.email,
                user_name=user.name,
                team=user.team,
                total_calories=total_calories,
                total_activities=total_activities
            )
        
        # Update ranks
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_calories')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()

        self.stdout.write('Creating workouts...')
        
        # Create workout suggestions
        workouts = [
            {
                'name': 'Super Soldier Training',
                'description': 'High-intensity workout inspired by Captain America training regimen',
                'difficulty': 'Advanced',
                'duration': 60,
                'target_calories': 700,
                'exercises': [
                    {'name': 'Push-ups', 'sets': 5, 'reps': 20},
                    {'name': 'Pull-ups', 'sets': 4, 'reps': 10},
                    {'name': 'Sprint intervals', 'sets': 6, 'duration': '30 seconds'},
                    {'name': 'Burpees', 'sets': 4, 'reps': 15},
                ]
            },
            {
                'name': 'Kryptonian Strength',
                'description': 'Build superhuman strength like Superman',
                'difficulty': 'Advanced',
                'duration': 75,
                'target_calories': 850,
                'exercises': [
                    {'name': 'Deadlifts', 'sets': 5, 'reps': 8},
                    {'name': 'Bench press', 'sets': 5, 'reps': 10},
                    {'name': 'Squats', 'sets': 5, 'reps': 12},
                    {'name': 'Military press', 'sets': 4, 'reps': 10},
                ]
            },
            {
                'name': 'Amazonian Warrior',
                'description': 'Combat training inspired by Wonder Woman',
                'difficulty': 'Intermediate',
                'duration': 50,
                'target_calories': 600,
                'exercises': [
                    {'name': 'Sword swings', 'sets': 4, 'reps': 20},
                    {'name': 'Shield holds', 'sets': 3, 'duration': '60 seconds'},
                    {'name': 'Lunge jumps', 'sets': 4, 'reps': 15},
                    {'name': 'Battle rope', 'sets': 4, 'duration': '30 seconds'},
                ]
            },
            {
                'name': 'Web-Slinger Agility',
                'description': 'Improve flexibility and agility like Spider-Man',
                'difficulty': 'Beginner',
                'duration': 40,
                'target_calories': 400,
                'exercises': [
                    {'name': 'Wall climbs', 'sets': 3, 'reps': 10},
                    {'name': 'Box jumps', 'sets': 4, 'reps': 12},
                    {'name': 'Spider crawls', 'sets': 3, 'duration': '45 seconds'},
                    {'name': 'Hanging knee raises', 'sets': 4, 'reps': 15},
                ]
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'Lightning-fast cardio workout inspired by The Flash',
                'difficulty': 'Intermediate',
                'duration': 45,
                'target_calories': 650,
                'exercises': [
                    {'name': 'Sprint intervals', 'sets': 8, 'duration': '30 seconds'},
                    {'name': 'High knees', 'sets': 5, 'reps': 30},
                    {'name': 'Mountain climbers', 'sets': 5, 'reps': 25},
                    {'name': 'Jump rope', 'sets': 4, 'duration': '2 minutes'},
                ]
            },
            {
                'name': 'Gotham Guardian',
                'description': 'Martial arts and detective work inspired by Batman',
                'difficulty': 'Advanced',
                'duration': 70,
                'target_calories': 750,
                'exercises': [
                    {'name': 'Shadow boxing', 'sets': 5, 'duration': '3 minutes'},
                    {'name': 'Grappling practice', 'sets': 4, 'duration': '5 minutes'},
                    {'name': 'Parkour drills', 'sets': 3, 'duration': '10 minutes'},
                    {'name': 'Core work', 'sets': 4, 'reps': 20},
                ]
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated database with superhero test data!'))
        self.stdout.write(f'Created {User.objects.count()} users')
        self.stdout.write(f'Created {Team.objects.count()} teams')
        self.stdout.write(f'Created {Activity.objects.count()} activities')
        self.stdout.write(f'Created {Leaderboard.objects.count()} leaderboard entries')
        self.stdout.write(f'Created {Workout.objects.count()} workouts')
