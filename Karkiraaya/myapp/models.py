from django.db import models
from django.contrib.auth.models import AbstractUser

class Car_details(models.Model):
    c_img=models.FileField(null=True)
    c_name=models.CharField(max_length=20,null=True)
    c_price=models.BigIntegerField(null=True)
    c_details=models.TextField(max_length=1000,null=True)
    c_status=models.IntegerField(null=True)
    


class User(AbstractUser):
    phone=models.BigIntegerField(null=True)
    type=models.IntegerField(null=True)
    rentedcar=models.ForeignKey(Car_details,on_delete=models.CASCADE,null=True)

class Deliveryandreturn(models.Model):
    cid=models.IntegerField(null=True)
    dplace=models.CharField(max_length=100,null=True)
    rplace=models.CharField(max_length=100,null=True)
    rcarid=models.IntegerField(null=True)
    fdate=models.DateField(null=True)
    rdate=models.DateField(null=True)
    license=models.CharField(max_length=20,null=True)

class Feedbacks(models.Model):
    name=models.CharField(max_length=20,null=True)
    describe=models.TextField(max_length=1200,null=True)
    date=models.DateTimeField(auto_now_add=True)


 