from django.contrib.auth import get_user_model
from rest_framework import viewsets
from api.v1.serializers import CompanySerializer, UserSerializer, CompanySerializerNotAuth
from companys.models import Company
from api.v1.permissions import IsAdminOnly, IsUser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

User = get_user_model()


"""
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ListaGruppi
        if self.action == 'retrieve':
            return serializers.DettaglioGruppi
        return serializers.Default  # I dont' know what you want for create/destroy/update.                
"""


class CompanyViewSet(viewsets.ViewSet):

    def get_user_company(self, request):
        try:
            user_company = request.user.profile.company.id
        except:
            user_company = None
        return user_company

    def get_user_role(self, request):
        try:
            user_role = request.user.profile.role
        except:
            user_role = None
        return user_role

    def list(self, request):
        queryset = Company.objects.all()
        if request.user.is_superuser:
            serializer = CompanySerializer(queryset, many=True)
        elif request.user.is_authenticated:
            try:
                if request.user.profile.role == 'admin':
                    serializer = CompanySerializer(queryset, many=True)
            except:
                pass
        else:
            serializer = CompanySerializerNotAuth(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user_company = self.get_user_company(request)

        if request.user.is_superuser or user_company:
            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        raise PermissionDenied({"message": "You don't have permission to access",
                                    "company_id": pk})

    def create(self, request):
        user_role = self.get_user_role(request)
        if request.user.is_superuser or user_role == 'admin':
            serializer = CompanySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        raise PermissionDenied({"message": "You don't have permission to create company"})

    def update(self, request, *args, **kwargs):
        user_role = self.get_user_role(request)
        user_company = self.get_user_company(request)

        instance = self.get_object()
        print(instance)
        serializer = CompanySerializer(
            instance=instance,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOnly, ]
