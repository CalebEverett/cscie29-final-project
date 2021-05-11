from .models import Application, Company, Reviewer
from .serializers import ApplicationSerializer, CompanySerializer, ReviewerSerializer
from rest_framework import viewsets


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows applications to be created, viewed, edited or deleted.
    """

    queryset = Application.objects.all().order_by("-created_date")
    serializer_class = ApplicationSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be created, viewed, edited or deleted.
    """

    queryset = Company.objects.all().order_by("-created_date")
    serializer_class = CompanySerializer


class ReviewerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviewers to be created, viewed, edited or deleted.
    """

    queryset = Reviewer.objects.all().order_by("-created_date")
    serializer_class = ReviewerSerializer
