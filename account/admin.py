from django.contrib import admin
from .models import User
from django.contrib.auth.hashers import is_password_usable
from .forms import UserForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )

    def save_model(self, request, obj: User, form: UserForm, change):
        if (
            form.is_valid()
            and obj.password != None
            and obj.password != ""
            and is_password_usable(obj.password)
        ):
            obj.set_password(obj.password)
        super(UserAdmin, self).save_model(request, obj, form, change)
