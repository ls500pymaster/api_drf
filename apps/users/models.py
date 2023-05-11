import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email'),
        max_length=254,
        unique=True,
        db_index=True,
        null=True,
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    class Language(models.TextChoices):
        ENGLISH = "en", "English"
        UKRAINIAN = "uk", "Ukrainian"
        RUSSIAN = "ru", "Russian"

    class Gender(models.TextChoices):
        MALE = "male", "MALE"
        FEMALE = "female", "FEMALE"

    first_name = models.CharField(_('first_name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, null=True, blank=True)
    default_language = models.CharField(max_length=2, choices=Language.choices)
    gender = models.CharField(max_length=6, choices=Gender.choices)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)

    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError(
                _("Password must have at least 8 characters"))

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.email:
            return self.email

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print(reset_password_token.__dict__)
    password_reset_url = f"{reverse('password_reset:reset-password-request')}?token={reset_password_token.key}"
    context = {"password_reset_url": password_reset_url}

    email_html_message = render_to_string("email/password_reset_email.html", context)
    email_plaintext_message = f"Please reset your password using this link {password_reset_url}"

    send_mail(
        # title:
        "Password Reset for BuildMuscleApp",
        # message:
        email_plaintext_message,
        # from:
        "admin@localhost.com",
        # to:
        [reset_password_token.user.email],
        # html_message:
        html_message=email_html_message,
    )