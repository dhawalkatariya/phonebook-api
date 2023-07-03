from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("phone_number",)


class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
