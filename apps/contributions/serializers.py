from rest_framework import serializers
from django.db.models import Sum
from .models import Contribution
from apps.accounts.models import Member

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = '__all__'

class MemberProfileSerializer(serializers.ModelSerializer):
    total_contributed = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ['id', 'username', 'email', 'kcse_year', 'total_contributed']

    def get_total_contributed(self, obj):
        # uses the related_name="my_contributions" defined in the Contribution model
        result = obj.my_contributions.aggregate(Sum('amount'))['amount__sum']
        return result or 0