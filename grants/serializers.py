from rest_framework import serializers

from .models import Application, Company, Reviewer


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewer
        fields = "__all__"
