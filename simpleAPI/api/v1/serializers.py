from django.contrib.auth import get_user_model
from rest_framework import serializers

from companys.models import Company, News

from users.models import Profile

User = get_user_model()


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    company_news = NewsSerializer(many=True, required=False)

    class Meta:
        model = Company
        exclude = ['id']

class CompanySerializerNotAuth(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['id', 'company_news']


class ProfileSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Profile
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'first_name', 'last_name', 'date_joined']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
