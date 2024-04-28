import logging
from django.shortcuts import render
from djoser.views import UserViewSet as DjoserUserViewSet
from .permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from .models import User
from .email import PasswordResetEmail
from .serializers import *


# Create your views here.
# ordinary user registration
class UserViewSet(DjoserUserViewSet):
    def perform_update(self, serializer):
        try:
            super().perform_update(serializer)
        except Exception as e:
            logging.exception("An error has occur while creating user")


# admin user registration
class AdminUserView(DjoserUserViewSet):
    """A view for creating, retrieving, updating, and deleting users (Admin-only)"""

    queryset = User.objects.all()
    serializer_class_create = AdminUserCreateSerializer  # create admin user
    serializer_class_retrieve = UserSerializer  # return this serializer afte creation

    def get_serializer_class(self):
        try:
            if self.action in ["list", "retrieve"]:
                return self.serializer_class_retrieve
            elif self.action == "create":
                return self.serializer_class_create
            return super().get_serializer_class()
        except Exception as e:
            logging.exception(
                "An error has occur while performing operation on  the admin view."
            )
            return Response(
                {"message": "An error has occur. Please contact the administrator"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserListAndDetail(ListAPIView, RetrieveAPIView, DestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer

    def get(self, request, pk=None):
        try:
            if pk:
                try:
                    user = User.objects.get(pk=pk)
                    serializer = self.serializer_class(user)
                    return Response(serializer.data)
                except User.DoesNotExist:
                    return Response(
                        {"message": "User not found."}, status=status.HTTP_404_NOT_FOUND
                    )
            else:
                queryset = User.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
        except Exception as e:
            logging.exception("An Error while fetching the users detail")
            return Response(
                {"messgae": "An error has occur. Please contact the administrator"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, pk=None):
        try:
            if pk:
                try:
                    user = User.objects.get(pk=pk)
                    user.delete()
                    return Response(
                        {"message": "User deleted successfully"},
                        status=status.HTTP_200_OK,
                    )
                except User.DoesNotExist:
                    return Response(
                        {"message": "User not found."}, status=status.HTTP_404_NOT_FOUND
                    )
        except Exception as e:
            logging.exception("An Error occur while deleting the users")
            return Response(
                {"messgae": "An error has occur. Please contact the administrator"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# login
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
