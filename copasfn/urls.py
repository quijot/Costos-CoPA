from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.urls import include, path

from .forms import AuthenticationFormCAPTCHA, EmailValidationOnForgotPassword

urlpatterns = [
    path("", include("costos.urls")),
    path("admin/", admin.site.urls),
    # override Login
    path(
        "accounts/login/",
        LoginView.as_view(form_class=AuthenticationFormCAPTCHA),
        name="login",
    ),
    # override Reset Password
    path(
        "accounts/password_reset/",
        PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword),
        name="password_reset",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]
# Developing
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [
        path("preferences/", include("dynamic_preferences.urls"))
    ]
