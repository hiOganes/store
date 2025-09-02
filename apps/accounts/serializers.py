from rest_framework import serializers
from django.core.exceptions import ValidationError

from apps.accounts.utils import check_password
from apps.accounts.models import User


class RegisterSerialier(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email exists")
        return value

    def validate_password(self, value):
        if not check_password(value):
            raise ValidationError("Short password")
        return value
