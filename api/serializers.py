from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import Spam

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        label=("Phone Number"),
        write_only=True
    )
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=("Token"),
        read_only=True
    )

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                msg = "Phone Number or password invalid"
                raise serializers.ValidationError(msg, code="authorization")

            if not check_password(password, user.password):
                msg = "Phone Number or password invalid"
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = ('Must include "phone_number" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        label=("Phone Number"),
        write_only=True
    )
    name = serializers.CharField(max_length=255, label=("Name"), required=True)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                phone_number=validated_data['phone_number'],
                name=validated_data['name'],
                email=validated_data.get('email'),
                password=validated_data['password'],
            )
            return user
        except IndentationError:
            raise serializers.ValidationError("Phone number already exists.")


class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = ('reported_number',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'name')


class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'email', 'name')
