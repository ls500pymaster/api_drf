from django.urls import include
from django.urls import path

from .views import SignupView, LoginView, LastLoginView, LastRequestView

urlpatterns = [
	path("signup/", SignupView.as_view(), name="signup"),
	path("login/", LoginView.as_view(), name="login"),

	path('api/<int:pk>/last-login/', LastLoginView.as_view(), name='last_login'),
	path('api/<int:pk>/last-request/', LastRequestView.as_view(), name='last_request'),
]