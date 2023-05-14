from django.utils import timezone
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

from .models import UserActivity


class LastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')

        if header is not None:
            token_string = header.split()[1]
            try:
                token = AccessToken(token_string)
            except (InvalidToken, TokenError) as e:
                print(f"Invalid token: {e}")  # Handle this as per your needs
            else:
                user_id = token["user_id"]
                UserActivity.objects.update_or_create(
                    user_id=user_id,
                    defaults={"last_request_time": timezone.now()}
                )
        response = self.get_response(request)
        return response
