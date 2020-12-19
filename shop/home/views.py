from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import (login,authenticate,logout)
from django.conf import settings 
from django.core.mail import send_mail 
import math,random,string
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
        TYPE=str(request.POST.get('type'))
        print(TYPE)
        if TYPE=="1":
            try:
                user=User.objects.get(email=email)
                return render(request,"home/signup_page.html",context={"email_verification": True, "otp_verification": False, "signup_details": False, "email_matched": True})
            except:
                pass
        else:
            try:
                user=User.objects.get(email=email)
            except:
                return render(request,"home/forgot_password_page.html",context={"email_verification": True, "otp_verification": False, "reser_password": False, "email_does_not_exist": True})
        otp=generateOTP()
        if TYPE=="1":
            subject = 'OTP for email verification in AIYAGRAMART'
            message = f'Hi user, thank you for creating account, your otp is ' + str(otp) + ', do not share it with anyone.\nThanks'
        else:
            subject = 'OTP for reseting the password in AIYAGRAMART'
            message = f'Hi user, otp to reset the password is ' + str(otp) + ', do not share it with anyone.\nThanks'
        SendMail(subject,message,email)
        try:
            user=OTP.objects.get(email=email)
            user.otp=otp
            user.date=datetime.datetime.now()
            user.save()
        except:
            OTP.objects.create(email=email, otp=otp, date=datetime.datetime.now)
        if TYPE=='1':
            return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": True, "signup_details": False, "email": email})
        else:
            return render(request,"home/forgot_password_page.html",context={"email_verification": False, "otp_verification": True, "reset_password": False, "email": email})
    else:
        return redirect('home')

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
        TYPE=str(request.POST.get('type'))
        user=OTP.objects.get(email=email)
        if str(user.otp)==otp:
            prev_date=user.date
            user.date=datetime.datetime.now()
            user.save()
            new_date=user.date
            user.date=prev_date
            user.save()
            time_delta = (new_date-prev_date)
            total_seconds = time_delta.total_seconds()
            minutes = total_seconds/60
            if(minutes>15):
                otp=generateOTP()
                if TYPE=="1":
                    subject = 'OTP for email verification in AIYAGRAMART'
                    message = f'Hi user, thank you for creating account is ' + str(otp) + ', do not share it with anyone.\nThanks'
                else:
                    subject = 'OTP for reseting the password in AIYAGRAMART'
                    message = f'Hi user, otp to reset the password is ' + str(otp) + ', do not share it with anyone.\nThanks'
                SendMail(subject,message,email)
                user.otp=otp=otp
                user.date=datetime.datetime.now()
                user.save()
                if TYPE=="1":
                    return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": True, "signup_details": False, "email": email, "time_exceeded": True})
                return render(request,"home/forgot_password_page.html",context={"email_verification": False, "otp_verification": True, "reset_password": False, "email": email, "time_exceeded": True})
            else:
                if TYPE=="1":
                    return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": False, "signup_details": True, "email": email})
                return render(request,"home/forgot_password_page.html",context={"email_verification": False, "otp_verification": False, "reset_password": True, "email": email})
        else:
            if TYPE=="1":
                return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": True, "signup_details": False, "email": email, "wrong_otp": True})
            return render(request,"home/forgot_password_page.html",context={"email_verification": False, "otp_verification": True, "reset_password": False, "email": email, "wrong_otp": True})
        
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
            checker = User.objects.get(username=username)
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
            return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": False, "signup_details": True, "prev": True, "email": email, "username_matched": True,"prev_username": res, "prev_first_name": first_name, "prev_last_name": last_name})
        except:
            if form.is_valid():
                password = request.POST.get("password2")
                user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                return render(request,"home/home.html",context={"signup_success": True})
            else:
                return render(request,"home/signup_page.html",context={"email_verification": False, "otp_verification": False, "signup_details": True, "email": email, "prev": True, "prev_username": username, "prev_first_name": first_name, "prev_last_name": last_name, "password_error": True, "error": form.errors})
    else:
        return redirect('signup_page')

def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def login_page(request):
    return render(request,"home/login_page.html",context={"standard_message": True})
 
def login_request(request):
    if request.method=="POST":
        useremail=request.POST.get('UserEmail')
        password=request.POST.get('password')
        try:
            checker = User.objects.get(username=useremail)
            user = authenticate(request, username=useremail, password=password)
            if user is not None:
                login(request, user)
                login_email(user.email)
                return redirect('home')
            else:
                return render(request,"home/login_page.html",context={"useremail": useremail, "Incorrect_Password": True})
        except:
            try:
                checker = User.objects.get(email=useremail)
                user = authenticate(request, username=checker.username, password=password)
                if user is not None:
                    login(request, user)
                    login_email(user.email)
                    return redirect('home')
                else:
                    return render(request,"home/login_page.html",context={"useremail": useremail, "Incorrect_Password": True})
            except:
                return render(request,"home/login_page.html",context={"Invalid_user_email": True})
    else:
        return HttpResponse("400 ERROR: Request Rejected to this url")

def login_email(email):
    subject = 'Successful Login in AIYAGRAMART'
    message = f'Hi user, thank you for logging in AIYAGRAMART.\nThanks'
    SendMail(subject,message,email)

def forgot_password_page(request):
    return render(request,"home/forgot_password_page.html",context={"email_verification": True, "otp_verification": False, "reset_password": False})

def reset_password(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password2")
        user=User.objects.get(email=email)
        user.set_password(password)
        user.save()
        subject = 'Password changed in AIYAGRAMART'
        message = f'Hi user, password has been successfully changed.\nThanks'
        SendMail(subject,message,email)
        return redirect('home')
    else:
        return redirect('forgot_password_page')