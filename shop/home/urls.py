from django.urls import path
from .views import home,signup_page,emailverification,otpverification,signupdetails,logout_request,login_request,login_page

urlpatterns = [
    path('',home,name='home'),
    path('signup_page/',signup_page,name="signup_page"),
    path('emailverification/',emailverification,name="emailverification"),
    path('otpverification/',otpverification,name="otpverification"),
    path('signupdetails/',signupdetails,name="signupdetails"),
    path('logout_request/',logout_request,name="logout_request"),
    path('login_request/',login_request,name="login_request"),
    path('login_page/',login_page,name="login_page"),
]