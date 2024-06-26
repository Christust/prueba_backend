from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["created_at", "updated_at", "last_login"]

    def create(self, validated_data):
        branches = []
        if validated_data.get("branches") != None:
            branches = validated_data.pop("branches")
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        for branch in branches:
            user.branches.add(branch)
        return user


class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "created_at", "updated_at", "last_login"]


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=120, min_length=6)
    password_confimation = serializers.CharField(max_length=120, min_length=6)

    def validate(self, data):
        current_user = self.context["current_user"]
        user = self.context["user"]
        if current_user != user and not current_user.is_superuser:
            raise serializers.ValidationError(
                {"user": "Debe ser superadmin o el usuario a cambiar"}
            )
        if data["password"] != data["password_confimation"]:
            raise serializers.ValidationError(
                {"password": "Debe ingresar la misma contraseña"}
            )
        return data


class CustomTokenObtainPairSerializer():
    pass
