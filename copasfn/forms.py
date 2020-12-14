from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm


class AuthenticationFormCAPTCHA(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3())


class EmailValidationOnForgotPassword(PasswordResetForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3())

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not get_user_model().objects.filter(email__iexact=email, is_active=True).exists():
            error_message = "No existe ningún usuario con esa dirección de correo electrónico."
            self.add_error("email", error_message)
        return email
