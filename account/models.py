from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.validators import RegexValidator


# Create your models here.


class UserManager(BaseUserManager):
    """Create super user"""

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


name_validator = RegexValidator(
    regex=r"^[a-zA-Z]+$",
    message="Name must contain only letters and no spaces.",
)

contact_number_validator = RegexValidator(
    regex=r"^\+?[0-9]+$",
    message="Contact number must contain only digits and an optional plus sign.",
)


class User(AbstractBaseUser, PermissionsMixin):
    user_roles = [("user", "user"), ("admin", "admin")]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, validators=[name_validator])
    last_name = models.CharField(max_length=100, validators=[name_validator])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    contact_number = models.CharField(
        max_length=20, null= True, blank=True, unique= True, validators=[contact_number_validator]
    )
    country = models.CharField(max_length=1000)
    role = models.CharField(max_length=50, choices=user_roles, default="user")
    date_joined = models.DateTimeField(auto_now_add=True)

    # Add related_name to resolve reverse accessor clashes
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    USERNAME_FIELD = "email"  #'username'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email
