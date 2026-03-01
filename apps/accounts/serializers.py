from rest_framework import serializers
from .models import Member
from django.db.models import Sum

class MemberSerializer(serializers.ModelSerializer):
    # password is write_only so it never shows up in GET requests
    password = serializers.CharField(write_only=True)
    total_contributed = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'kcse_year', 'sponsor_name', 'total_contributed']

    def get_total_contributed(self, obj):
        result = obj.my_contributions.aggregate(Sum('amount'))['amount__sum']
        return result or 0

    def create(self, validated_data):
        # Use create_user to ensure the password is hashed correctly
        return Member.objects.create_user(**validated_data)