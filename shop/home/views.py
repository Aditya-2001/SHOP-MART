from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import (login,authenticate,logout)
from django.conf import settings 
from django.core.mail import send_mail 
import math,random
from .models import OTP
import datetime
from .forms import UserForm
# Create your views here.
def home(request):
    return render(request,"home/home.html",context={})

def signup_page(request):
    return render(request,"home/signup_page.html",context={"email_verification": True, "otp_verification": False, "signup_details": False})

def emailverification(request):
    if request.method=="POST":
        email=request.POST.get('email')
        otp=generateOTP()
        subject = 'OTP for email verification in AIYAGRAMART'
        message = f'Hi user, thank you for creating account is ' + str(otp) + ', do not share it with anyone.\nThanks'
        SendMail(subject,message,email)
        try:
            user=OTP.objects.get(email=email)
            user.otp=otp
            user.date=datetime.datetime.now()
            user.save()
        except:
            OTP.objects.create(email=email, otp=otp, date=datetime.datetime.now)
        return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": True, "signup_details": False, "email": email})
        
    else:
        return redirect('signup_page')

def generateOTP() : 
    digits = "0123456789"
    OTP = "" 
    for i in range(6) : 
        OTP += digits[math.floor(random.random() * 10)] 
    return int(OTP)

def SendMail(subject, message, email):
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [email, ] 
    send_mail( subject, message, email_from, recipient_list ) 

def otpverification(request):
    if request.method=="POST":
        email=request.POST.get('email')
        otp=str(request.POST.get('otp'))
        print(email)
        try:
            user=OTP.objects.get(email=email)
            if str(user.otp)==otp:
                current_date=datetime.datetime.now()
                expected_otp_sent_time=user.otp
                time_delta = (current_date-expected_otp_sent_time)
                total_seconds = time_delta.total_seconds()
                minutes = total_seconds/60
                if(minutes>15):
                    otp=generateOTP()
                    subject = 'OTP for email verification in AIYAGRAMART'
                    message = f'Hi user, thank you for creating account is ' + str(otp) + ', do not share it with anyone.\nThanks'
                    SendMail(subject,message,email)
                    user.otp=otp=otp
                    user.date=datetime.datetime.now()
                    user.save()
                    print('1111111111111111111111111111111111111111')
                    return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": True, "signup_details": False, "email": email, "time_exceeded": True})
                else:
                    print('222222222222222222222222222')
                    return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": False, "signup_details": True, "email": email})
            else:
                print('22233333333333333333333333333333333333333332')
                return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": True, "signup_details": False, "email": email, "wrong_otp": True})
        except:
            print('224444444444444444444444444444444444444442')
            return render(request,"home/signup_page.html",context={"email_verification": True, "otp_verification": False, "signup_details": False, "email": email, "email_not_found": True})
        
    else:
        return redirect('signup_page')

def signupdetails(request):
    if request.method=="POST":
        form = UserForm(request.POST)
        username=request.POST.get("username")
        email=request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")   
        try:
            checker = User.objects.get(email=email)
            return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": False, "signup_details": True, "prev": True, "email": email, "email_matched": True, "prev_username": username, "prev_first_name": first_name, "prev_last_name": last_name})
        except:
            try:
                checker = User.objects.get(username=username)
                return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": False, "signup_details": True, "prev": True, "email": email, "username_matched": True,"prev_username": "", "prev_first_name": first_name, "prev_last_name": last_name})
            except:
                if form.is_valid():
                    password = request.POST.get("password2")
                    user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
                    user.set_password(password)
                    user.save()
                    return redirect('home')
                else:
                    return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": False, "signup_details": True, "email": email, "password_error": True, "error": form.errors})
        
    else:
        return redirect('signup_page')
