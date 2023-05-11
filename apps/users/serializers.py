from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = "__all__"


class UserSigninSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			"email",
			"first_name",
			"last_name",
		)


class UserSignupSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("email", "first_name", "password",)
		extra_kwargs = {"password": {"write_only": True}}

	def create(self, validated_data):
		user = User(
			email=validated_data["email"],
			first_name=validated_data["first_name"],
		)
		user.set_password(validated_data["password"])
		user.save()
		return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		data = super().validate(attrs)

		user_serializer = UserSigninSerializer(self.user)

		data.update(
			{
				"user": user_serializer.data,
				"access_token": data.pop("access"),
				"refresh": data.pop("refresh"),
			}
		)
		return data
