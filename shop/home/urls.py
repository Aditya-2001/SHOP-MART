from django.urls import path
from .views import home,signup_page

urlpatterns = [
    path('',home,name='home'),
    path('signup_page/',signup_page,name="signup_page"),
]