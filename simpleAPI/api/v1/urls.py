from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'companys', CompanyViewSet, basename='company')

urlpatterns = router_v1.urls