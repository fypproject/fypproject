from django.db import models

# Create your models here.

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_myadmin = models.BooleanField(default=False)

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

class Student(models.Model):
    STATUS = (
        ('Active','Active'),
        ('Inactive','Inactive'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    s_phoneno=models.CharField(max_length=50,blank=True,null=True)
    s_city=models.CharField(max_length=50,blank=True,null=True)
    s_country=models.CharField(max_length=50,blank=True,null=True)
    s_image=models.ImageField(blank=True,null=True,upload_to='images/',default='images/default.jpg')
    s_regno=models.CharField(max_length=50,unique=True)
    s_parentscontact=models.CharField(max_length=50,blank=True,null=True)
    s_batchid=models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
    s_status=models.CharField(max_length=200,null=True,choices=STATUS,default="Active")
    def __str__(self):
    	return self.user.username

class Faculty(models.Model):
    STATUS = (
        ('Active','Active'),
        ('Inactive','Inactive'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    f_phoneno=models.CharField(max_length=50,blank=True,null=True)
    f_city=models.CharField(max_length=50,blank=True,null=True)
    f_country=models.CharField(max_length=50,blank=True,null=True)
    f_image=models.ImageField(blank=True,null=True,upload_to='images/')
    f_qualifications=models.CharField(max_length=50,null=True,blank=True)
    f_status=models.CharField(max_length=200,null=True,choices=STATUS,default="Active")

    
    def __str__(self):
    	return self.user.username

class myAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ad_phoneno=models.CharField(max_length=50,blank=True,null=True)
    ad_city=models.CharField(max_length=50,blank=True,null=True)
    ad_country=models.CharField(max_length=50,blank=True,null=True)
    ad_image=models.ImageField(blank=True,null=True,upload_to='images/')
   
    def __str__(self):
    	return self.user.username




class Course(models.Model):
    c_id=models.AutoField(primary_key=True)
    c_name=models.CharField(max_length=50)
    c_programid=models.ForeignKey(Program,on_delete=models.CASCADE)
    def __str__(self):
    	return self.c_name

class Bcf(models.Model):
    bcf_id=models.AutoField(primary_key=True)
    bcf_batchid=models.ForeignKey(Batch,on_delete=models.CASCADE)
    bcf_courseid=models.ForeignKey(Course,on_delete=models.CASCADE)
    bcf_facultyid=models.ForeignKey(User,on_delete=models.CASCADE)
   


class Lecture(models.Model):
    choice=(
        ('Announcement','Announcement'),
        ('Lecture','Lecture'),
    )
    l_id=models.AutoField(primary_key=True)
    l_name=models.CharField(max_length=255,choices=choice)
    l_desc=models.CharField(max_length=1000)
    l_file=models.FileField(blank=True,null=True,upload_to='lectures/')
    l_bcfid=models.ForeignKey(Bcf,on_delete=models.CASCADE)
    
class Assignment(models.Model):
    a_id=models.AutoField(primary_key=True)
    a_name=models.CharField(max_length=255)
    a_desc=models.CharField(max_length=1000)
    a_startdate=models.DateTimeField()
    a_enddate=models.DateTimeField()
    a_file=models.FileField(blank=True,null=True,upload_to='assignments/')
    a_mark=models.IntegerField()
    a_bcfid=models.ForeignKey(Bcf,on_delete=models.CASCADE)