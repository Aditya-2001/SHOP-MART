from django.db import models
import datetime 
# Create your models here.
class OTP(models.Model):
    email=models.EmailField(max_length=50)
    otp=models.IntegerField(default=-1)
    date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email