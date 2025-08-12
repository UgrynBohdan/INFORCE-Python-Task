from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count

from .models import Vote
from .serializers import VoteSerializer, VoteResultSerializer
from restaurants.models import Menu

# Create your views here.


# POST /api/votes/ — голосування
class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]


# GET /api/votes/results/today/ — результати голосування
class TodayVoteResultsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VoteResultSerializer

    def get_queryset(self):
        today = now().date()
        return (
            Menu.objects.filter(date=today)
            .annotate(votes_count=Count("votes"))
            .values("restaurant__name", "votes_count")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            [{"restaurant_name": item["restaurant__name"], "votes_count": item["votes_count"]} for item in queryset],
            many=True
        )
        return Response(serializer.data)
