from django.contrib.auth import get_user_model
from rest_framework import viewsets
from api.v1.serializers import CompanySerializer, UserSerializer, CompanySerializerNotAuth, NewsSerializer
from companys.models import Company, News
from api.v1.permissions import IsAdminOnly, IsUser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action


User = get_user_model()


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsAdminOnly|IsUser,]

    def get_serializer_class(self):
        try:
            role = self.request.user.profile.role
        except AttributeError:
            role = None
        if self.action == 'list' and role == 'admin':
            return CompanySerializer
        if self.action == 'my_company':
            return CompanySerializer
        if self.action == 'retrieve':
            return CompanySerializer
        return CompanySerializerNotAuth

    @action(detail=False, methods=['get', 'patch', 'put'], permission_classes=[IsUser|IsAdminOnly],
            url_path='my-company', url_name='my_company')
    def my_company(self, request):
        company = Company.objects.filter(pk=request.user.profile.company.id)

        page = self.paginate_queryset(company)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(company, many=True)
        return Response(serializer.data)


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    permission_classes = [IsAdminOnly|IsUser]

    def get_queryset(self):
        company = Company.objects.get(pk=self.request.user.profile.company.id)
        return News.objects.filter(company=company)



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOnly, ]


