from django.urls import path,include,re_path
from accounts.views import *
import knox.views as knox_views
urlpatterns = [
    path('validate_phone/',ValidatePhoneSendOTP.as_view()),
    path('validate_phone_forgot/',ValidatePhoneForgot.as_view()),
    re_path("^validate_otp/$",ValidateOTP.as_view()),
    re_path("^validate_otp_forgot/$",ForgotValidateOTP.as_view()),
    re_path("^forgot_password_change/$",ForgetPasswordChange.as_view()),
    re_path("^register/$",Register.as_view()),
    re_path("^login/$",LoginAPI.as_view()),
    re_path("^logout/$",knox_views.LogoutView.as_view()),

]