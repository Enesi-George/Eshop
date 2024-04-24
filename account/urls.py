from django.urls import path

from rest_framework_simplejwt import views as simple_jwt_views

from .views import UserViewSet, AdminUserView, MyTokenObtainPairView

urlpatterns= [
    # path("login/", simple_jwt_views.TokenObtainPairView.as_view(), name="login"),  
    path("login/", MyTokenObtainPairView.as_view(), name="login"),  
    path("refresh/", simple_jwt_views.TokenRefreshView.as_view(), name="refresh-token"),
    path("verify/", simple_jwt_views.TokenVerifyView.as_view(), name="verify-token"),
    path('register/', UserViewSet.as_view({"post": "create"}), name='register'),
    path('register-admin/', AdminUserView.as_view(), name='register-admin'),
    path('me/', UserViewSet.as_view({"get": "me", "delete": "me", "patch": "me", "put": "me"}), name='me'),
    path("activation/<str:uid>/<str:token>/", UserViewSet.as_view({"post": "activation"}), name="activation"),		#to make user become active
    path("resend-activation/", UserViewSet.as_view({"post": "resend_activation"}), name="resend-activation"),
    path("forgot-password/", UserViewSet.as_view({"post": "reset_password"}), name="forgot-password"),
    path("change-password/", UserViewSet.as_view({"post": "set_password"}), name="change-password"),
    path("confirm-password-reset/", UserViewSet.as_view({"post": "reset_password_confirm"}), name="confirm-password-reset")
]
