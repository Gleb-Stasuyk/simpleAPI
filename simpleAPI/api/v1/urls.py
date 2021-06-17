from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, UserViewSet, NewsViewSet

router_v1 = DefaultRouter(trailing_slash=True)
router_v1.register(r'users', UserViewSet, basename='user',)
router_v1.register(r'companys', CompanyViewSet, basename='company')
router_v1.register(
    r'companys/my_company/news',
    NewsViewSet,
    basename='news'
)

urlpatterns = router_v1.urls