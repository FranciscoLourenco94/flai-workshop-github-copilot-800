from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'team', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def get_id(self, obj):
        return str(obj.id) if obj.id else None


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at', 'member_count']

    def get_id(self, obj):
        return str(obj.id) if obj.id else None

    def get_member_count(self, obj):
        return User.objects.filter(team=obj.name).count()


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'user_email', 'activity_type', 'duration', 'calories', 'date', 'created_at']

    def get_id(self, obj):
        return str(obj.id) if obj.id else None


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user = serializers.CharField(source='user_name', read_only=True)
    total_points = serializers.IntegerField(source='total_calories', read_only=True)
    activity_count = serializers.IntegerField(source='total_activities', read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user_email', 'user_name', 'user', 'team', 'total_calories', 'total_points', 'total_activities', 'activity_count', 'rank']

    def get_id(self, obj):
        return str(obj.id) if obj.id else None


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty', 'duration', 'target_calories', 'exercises']

    def get_id(self, obj):
        return str(obj.id) if obj.id else None
