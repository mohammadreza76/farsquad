from django.urls import path,re_path
from accounts.views import *
import knox.views as knox_views
from accounts import views #phase2

try:
    urlpatterns = [
        path('validate_phone',views.ValidatePhoneSendOTP.as_view()),
        path('validate_phone_forgot',views.ValidatePhoneForgot.as_view()),
        re_path("^validate_otp/$",views.ValidateOTP.as_view()),
        re_path("^validate_otp_forgot/$",views.ForgotValidateOTP.as_view()),
        re_path("^forgot_password_change/$",views.ForgetPasswordChange.as_view()),
        re_path("^register/$",Register.as_view()),
        re_path("^login/$",LoginAPI.as_view()),
        re_path("^logout/$",knox_views.LogoutView.as_view()),
        path('profile/<slug>', views.ProfileDetailView.as_view(), name='profile-detail'),#phase 2
        path('profiles', views.ProfileListView.as_view(), name='profiles-list'),#phase 2
        path('scores/<slug>', views.show_score, name='scores-user'),#phase 2.5
    ]
except:
     urlpatterns=[]   