from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .models import UserActivity


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
		fields = ("email",
		          "first_name",
		          "password",)
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

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'default_language': self.user.default_language,
            'gender': self.user.gender,
            'age': self.user.age,
        }

        return data

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#
# 	def validate(self, attrs):
# 		data = super().validate(attrs)
#
# 		user_serializer = UserSigninSerializer(self.user)
#
# 		data.update(
# 			{
# 				"user": user_serializer.data,
# 				"access_token": data.pop("access"),
# 				"refresh": data.pop("refresh"),
# 			}
# 		)
# 		return data
#
# 	@classmethod
# 	def get_token(cls, user):
# 		token = super().get_token(user)
#
# 		# Update user's last login time
# 		update_last_login(None, user)
#
# 		return token


class UserActivitySerializer(serializers.ModelSerializer):
	class Meta:
		model = UserActivity
		fields = ("last_login",
		          "last_request_time",)

