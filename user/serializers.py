from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext as _


class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    birth_date = serializers.DateField(required=True)
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        style={"input_type": "password"}
    )

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "birth_date",
        )
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5}
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "birth_date",
            "is_staff",
        )
        read_only_fields = ("id", "is_staff")

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=5)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Wrong old password!")
        return value

    def validate(self, data):
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as old one."})
        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
