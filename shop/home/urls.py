from django.urls import path
from .views import home,signup_page,emailverification,otpverification,signupdetails

urlpatterns = [
    path('',home,name='home'),
    path('signup_page/',signup_page,name="signup_page"),
    path('emailverification/',emailverification,name="emailverification"),
    path('otpverification/',otpverification,name="otpverification"),
    path('signupdetails/',signupdetails,name="signupdetails"),
]