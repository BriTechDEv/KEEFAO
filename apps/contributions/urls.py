from django.urls import path
from .views import (
    ContributionCreateView, 
    ContributionSummaryView, 
    UserContributionHistoryView,
    ContributionLeaderboardView,
    ClassYearLeaderboardView
)

urlpatterns = [
    path("create/", ContributionCreateView.as_view(), name="contribution-create"),
    path("summary/", ContributionSummaryView.as_view(), name="contribution-summary"),
    path("my-history/", UserContributionHistoryView.as_view(), name="my-contributions"),
    path("leaderboard/members/", ContributionLeaderboardView.as_view(), name="member-leaderboard"),
    path("leaderboard/classes/", ClassYearLeaderboardView.as_view(), name="class-leaderboard"),
]