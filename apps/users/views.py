from django.shortcuts import render
from .models import UserActivity
from .serializers import UserActivitySerializer
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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


class LastLoginView(generics.GenericAPIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		user_id = self.kwargs["pk"]
		user = User.objects.get(id=user_id)
		return Response({"last_login": user.last_login})


class LastRequestView(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request, pk, format=None):
		user_activity = UserActivity.objects.get(user_id=pk)
		serializer = UserActivitySerializer(user_activity)
		return Response(serializer.data)
