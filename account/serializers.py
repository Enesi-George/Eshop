import requests
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        required=True, min_length=8, write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'country', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_confirm_password(self, value):
        if self.initial_data.get("password") != value:
            raise serializers.ValidationError("The password and confirm password do not match.")
        return value

    def validate_country(self, value):
        # Fetch list of countries from REST Countries API
        response = requests.get("https://restcountries.com/v3.1/all")
        countries = [country["name"]["common"] for country in response.json()]

        # Validate selected country
        if value not in countries:
            raise serializers.ValidationError("Invalid country selection.")
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = User.objects.create_user(**validated_data)
        return user
