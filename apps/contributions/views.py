from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import Contribution
from .serializers import ContributionSerializer
from apps.accounts.models import Member

class ContributionCreateView(generics.CreateAPIView):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer

    # Optional: Automatically link the contribution to the logged-in user
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(member=self.request.user)
        else:
            serializer.save()

class ContributionSummaryView(APIView):
    """
    Returns total amounts and counts grouped by category.
    """
    def get(self, request):
        summary = Contribution.objects.values('category').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')

        grand_total = Contribution.objects.aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            "grand_total": grand_total,
            "breakdown": summary
        })

class UserContributionHistoryView(generics.ListAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contribution.objects.filter(member=self.request.user).order_by('-created_at')
    
class ContributionLeaderboardView(APIView):
    """
    Returns the top 10 members based on total contributions.
    """
    def get(self, request):
        # We query Members, sum their contributions, and filter out those with 0
        leaderboard = Member.objects.annotate(
            total_donated=Sum('my_contributions__amount')
        ).filter(
            total_donated__gt=0
        ).order_by('-total_donated')[:10]  # Get Top 10

        data = [
            {
                "username": member.username,
                "kcse_year": member.kcse_year,
                "total_donated": member.total_donated
            }
            for member in leaderboard
        ]

        return Response(data)
    
class ClassYearLeaderboardView(APIView):
    """
    Groups contributions by the member's KCSE year to see which class has raised the most.
    """
    def get(self, request):
        # We group by the KCSE year of the member and sum the amounts
        # Note: We filter for only contributions that are linked to a member
        class_stats = Contribution.objects.filter(member__isnull=False).values(
            'member__kcse_year'
        ).annotate(
            total_raised=Sum('amount')
        ).order_by('-total_raised')

        data = [
            {
                "kcse_year": item['member__kcse_year'],
                "total_raised": item['total_raised']
            }
            for item in class_stats
        ]

        return Response(data)