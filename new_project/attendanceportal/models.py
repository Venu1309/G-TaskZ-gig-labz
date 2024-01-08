from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self) :
        return self.name

class CustomUser(AbstractUser):
    phonenumber = models.CharField(max_length=15)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

class OTP(models.Model):
    otp = models.CharField(max_length=6)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


