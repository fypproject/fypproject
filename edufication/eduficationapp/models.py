from django.db import models

# Create your models here.

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_myadmin = models.BooleanField(default=False)
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    s_phoneno=models.CharField(max_length=50,blank=True,null=True)
    s_city=models.CharField(max_length=50,blank=True,null=True)
    s_country=models.CharField(max_length=50,blank=True,null=True)
    s_image=models.ImageField(blank=True,null=True)
    s_regno=models.CharField(max_length=50,unique=True)
    s_statusid=models.IntegerField(default=2)
    s_parentscontact=models.CharField(max_length=50)
    s_batchid=models.IntegerField()
    def __str__(self):
    	return self.user.username

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    f_phoneno=models.CharField(max_length=50,blank=True,null=True)
    f_city=models.CharField(max_length=50,blank=True,null=True)
    f_country=models.CharField(max_length=50,blank=True,null=True)
    f_image=models.ImageField(blank=True,null=True)
    f_qualifications=models.CharField(max_length=50,null=True,blank=True)

    
    def __str__(self):
    	return self.user.username

class myAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ad_phoneno=models.CharField(max_length=50,blank=True,null=True)
    ad_city=models.CharField(max_length=50,blank=True,null=True)
    ad_country=models.CharField(max_length=50,blank=True,null=True)
    ad_image=models.ImageField(blank=True,null=True)
   
    def __str__(self):
    	return self.user.username


class Program(models.Model):
    p_id=models.AutoField(primary_key=True)
    p_name=models.CharField(max_length=50)
    def __str__(self):
    	return self.p_name

class Batch(models.Model):
    b_id=models.AutoField(primary_key=True)
    b_name=models.CharField(max_length=50)
    b_programid=models.ForeignKey(Program,on_delete=models.CASCADE)
    def __str__(self):
    	return self.b_name

class Course(models.Model):
    c_id=models.AutoField(primary_key=True)
    c_name=models.CharField(max_length=50)
    c_programid=models.ForeignKey(Program,on_delete=models.CASCADE)
    def __str__(self):
    	return self.c_name









# class myAdmin(models.Model):
#     ad_id=models.AutoField
#     ad_fname=models.CharField(max_length=50)
#     ad_email=models.CharField(max_length=100,unique=True)
#     ad_uname=models.CharField(max_length=50,unique=True)
#     ad_password=models.CharField(max_length=50)
#     ad_phoneno=models.CharField(max_length=50,null=True,blank=True)
#     ad_city=models.CharField(max_length=50,null=True,blank=True)
#     ad_country=models.CharField(max_length=50,null=True,blank=True)
#     ad_image=models.ImageField(upload_to="adminprofile/images",null=True,blank=True)

#     def __str__(self):
#         return self.ad_fname
    
