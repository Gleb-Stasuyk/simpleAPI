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

    def update(self, instance, validated_data):

        profile_data = validated_data.pop('profile')
        profile = instance.profile

        # * User Info
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)

        # * AccountProfile Info
        profile.company = profile_data.get(
            'company', profile.company)
        profile.bio = profile_data.get(
            'bio', profile.bio)
        profile.location = profile_data.get(
            'location', profile.location)
        profile.birth_date = profile_data.get(
            'birth_date', profile.birth_date)
        profile.role = profile_data.get(
            'role', profile.role)
        profile.save()

        return instance
