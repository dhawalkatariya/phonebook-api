from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.constraints import UniqueConstraint
from .managers import CustomUserManager


# Create your models here.

class User(AbstractUser):
    username = None
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=128)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10}$', message="Please Enter Valid Phone Number")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=10, unique=True, primary_key=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["password", "name"]

    objects = CustomUserManager()


class Contact(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10}$', message="Please Enter Valid Phone Number")
    saved_contact = models.CharField(
        validators=[phone_regex], max_length=10, blank=True)
    saved_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [UniqueConstraint(
            "user", "saved_contact", name="user_contact_pair")]


class Spam(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10}$', message="Please Enter Valid Phone Number")
    reported_number = models.CharField(validators=[phone_regex], max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [UniqueConstraint("user", "reported_number",
                                        name="user_reported_number")]
