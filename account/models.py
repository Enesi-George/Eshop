from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone

name_validator = RegexValidator(
    regex=r"^[a-zA-Z]+$",
    message="Name must contain only letters and no spaces.",
)
username_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9]+$",
    message="Username must contain only letters and numbers with no spaces.",
)
mobile_number_validator = RegexValidator(
    regex=r"^\+\d{12}$",
    message="Mobile number must be in the format: '+2348176084667'.",
)

PASSWORD_VALIDATOR = RegexValidator(
        regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+])[a-zA-Z\d!@#$%^&*()_+]{8,}$',
        message="Password must be at least 8 characters long and contain at least one digit, one lowercase letter, one uppercase letter, and one special character."
    )

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=150, null=False, blank=False, validators=[name_validator]
    )
    last_name = models.CharField(
        max_length=150, null=False, validators=[name_validator]
    )
    email = models.EmailField(unique=True, null=False, error_messages={'unique': 'A user with this email already exists.'})
    username = models.CharField(max_length=150, unique=True, null=False, validators=[username_validator], error_messages={'unique': 'A user with this username already exists.'})
    country = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(_('password'), max_length=128, validators=[PASSWORD_VALIDATOR])

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
