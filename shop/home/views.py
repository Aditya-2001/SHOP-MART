from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def home(request):
    return render(request,"home/home.html",context={})

def signup_page(request):
    return render(request,"home/signup_page.html",context={"email_verification": True, "otp_verification": False, "signup_details": False})