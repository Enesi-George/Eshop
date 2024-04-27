import requests
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from django.core.validators import RegexValidator


class BaseUserCreateSerializer(BaseUserCreateSerializer):
    password_validator = RegexValidator(
        regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
        message="Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, and one digit.",
    )

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "country",
            "password",
        ]

    def validate_password(self, value):
        self.password_validator(value)
        return value

    def validate_country(self, value):
        # Fetch list of countries from REST Countries API
        response = requests.get("https://restcountries.com/v3.1/all")
        countries = [country["name"]["common"] for country in response.json()]

        # Validate selected country
        if value not in countries:
            raise serializers.ValidationError("Invalid country selection.")
        return value


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = BaseUserCreateSerializer.Meta.fields

    def validate_country(self, value):
        return super().validate_country(value)


class AdminUserCreateSerializer(BaseUserCreateSerializer):
    role = serializers.CharField(default="admin")  # Set default value for role field
    class Meta(BaseUserCreateSerializer.Meta):
        fields = BaseUserCreateSerializer.Meta.fields + ["role", "is_active"]

    def validate_confirm_password(self, value):
        return super().validate_confirm_password(value)

    def validate_country(self, value):
        return super().validate_country(value)
    

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):

        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "country",
            "role",
            "is_superuser",
            "is_active",
            "date_joined",
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["role"] = user.role  # assuming a "role" field on the user model
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["is_staff"] = user.is_staff
        return token
