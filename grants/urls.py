from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"applications", views.ApplicationViewSet)
router.register(r"companies", views.CompanyViewSet)
router.register(r"reviewers", views.ReviewerViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
