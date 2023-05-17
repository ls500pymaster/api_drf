from django.urls import path, include

from .views import SignupView, LoginView, LastLoginView, LastRequestView

urlpatterns = [
	path("signup/", SignupView.as_view(), name="signup"),
	path("login/", LoginView.as_view(), name="login"),

	path('<int:pk>/last-login/', LastLoginView.as_view(), name='last_login'),
	path('<int:pk>/last-request/', LastRequestView.as_view(), name='last_request')
]