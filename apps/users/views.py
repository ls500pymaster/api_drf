from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSignupSerializer, UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()


class SignupView(APIView):

	def post(self, request, format=None):
		serializer = UserSignupSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			refresh = RefreshToken.for_user(user)
			user_serializer = UserSerializer(user)

			return Response(
				{
					"access_token": str(refresh.access_token),
					"refresh": str(refresh),
					"user": user_serializer.data,
				},
				status=status.HTTP_201_CREATED
			)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer