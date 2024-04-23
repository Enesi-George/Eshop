from django.urls import path
from .views import UserRegistration, UserLogin,UserList

urlpatterns = [
    path("sign-up", UserRegistration.as_view(), name="account-create"),
    path("users/login", UserLogin.as_view(), name="user-login"),
    path("view/all-users", UserList.as_view(), name="view-all-user")
]
