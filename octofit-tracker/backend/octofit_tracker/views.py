from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def by_email(self, request):
        email = request.query_params.get('email', None)
        if email:
            try:
                user = User.objects.get(email=email)
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Email parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=False, methods=['get'])
    def by_name(self, request):
        name = request.query_params.get('name', None)
        if name:
            try:
                team = Team.objects.get(name=name)
                serializer = self.get_serializer(team)
                return Response(serializer.data)
            except Team.DoesNotExist:
                return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Name parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user_email = request.query_params.get('user_email', None)
        if user_email:
            activities = Activity.objects.filter(user_email=user_email).order_by('-date')
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'user_email parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    @action(detail=False, methods=['post'])
    def update_rankings(self, request):
        # Update the leaderboard rankings based on total calories
        leaderboard = Leaderboard.objects.all().order_by('-total_calories')
        for index, entry in enumerate(leaderboard, start=1):
            entry.rank = index
            entry.save()
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'difficulty parameter required'}, status=status.HTTP_400_BAD_REQUEST)
