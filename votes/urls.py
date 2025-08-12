from django.urls import path
from .views import VoteCreateView, TodayVoteResultsView

urlpatterns = [
    path("", VoteCreateView.as_view(), name="vote"),
    path("results/today/", TodayVoteResultsView.as_view(), name="vote-results-today"),
]
