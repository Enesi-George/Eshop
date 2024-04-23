import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserRegistration(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered Successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.exception("An error occurred while creating user.")
            return Response({"message": "An error has occurred. Please contact the administrator."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.all()
            serializer = UserSerializer(user, many=True)
            return Response({"message": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception("An error occur while getting all users")
            return Response({"error": "A server error has occur.Please contact the administrator"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

