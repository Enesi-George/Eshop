from django.shortcuts import render
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.email import PasswordResetEmail as DjoserPasswordResetEmail

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import GenericAPIView
from os import path
from .permissions import IsAdminOrReadOnly, IsAdmin, IsSuperUser, IsOwner, IsOwnerOrReadOnly, CanCreateSuperAdmin
from .models import User
from .serializers import *
from urllib3.util import parse_url
from Eshop.settings import BASE_DIR, DEFAULT_APP_URL
# Create your views here.

class UserViewSet(DjoserUserViewSet):
	def perform_update(self, serializer):
		super().perform_update(serializer)
class PasswordResetEmail(DjoserPasswordResetEmail):
	template_name = path.join(BASE_DIR,  "templates/emails/password_reset.html")
	def get_context_data(self):
        # PasswordResetEmail can be deleted
		context = super().get_context_data()
		url = parse_url(DEFAULT_APP_URL)
		context["domain"] = url.hostname
		context["protocol"] = url.scheme
		print(f"{context['protocol']}{DEFAULT_APP_URL}")
		return context
		

class AdminUserView(GenericAPIView):
    """ A view for creating Admin users """
    queryset = User.objects.all()
    serializer_class = AdminUserCreateSerializer

    def post(self, request):
        data = {**request.data, "role": "admin"}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        print("I'm here")
        user = serializer.save()

        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
