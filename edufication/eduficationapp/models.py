from django.db import models
import os

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
    forget_password_token=models.CharField(max_length=100,default='')
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
    forget_password_token=models.CharField(max_length=100,default='')
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
    forget_password_token=models.CharField(max_length=100,default='')
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
    bcf_status=models.CharField(max_length=100,default="In Progress")
   


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
    
    def filename(self):
        return os.path.basename(self.a_file.name)

class Quiz(models.Model):
    q_id=models.AutoField(primary_key=True)
    q_name=models.CharField(max_length=255)
    q_startdate=models.DateTimeField()
    q_enddate=models.DateTimeField()
    q_question=models.IntegerField()
    q_bcfid=models.ForeignKey(Bcf,on_delete=models.CASCADE)

class QuizQuestion(models.Model):
    qq_id=models.AutoField(primary_key=True)
    qq_question= models.CharField(max_length=255)
    qq_option1=models.CharField(max_length=255)
    qq_option2=models.CharField(max_length=255)
    qq_option3=models.CharField(max_length=255)
    qq_option4=models.CharField(max_length=255)
    qq_marks=models.IntegerField()
    qq_correctanswer=models.CharField(max_length=255)
    qq_quizid=models.ForeignKey(Quiz,on_delete=models.CASCADE)


class Attendance(models.Model):
    at_id=models.AutoField(primary_key=True)
    at_name=models.CharField(max_length=255)
    at_date=models.DateField()
    at_bcfid=models.ForeignKey(Bcf,on_delete=models.CASCADE)

class AttendanceRecord(models.Model):
    options=(
        ('Present','Present'),
        ('Absent','Absent'),
        ('Late','Late'),
        ('Excused','Excused'),
    )
    atr_id=models.AutoField(primary_key=True)
    atr_studentid=models.ForeignKey(User,on_delete=models.CASCADE)
    atr_option=models.CharField(max_length=255,choices=options)
    atr_atid=models.ForeignKey(Attendance,on_delete=models.CASCADE)


class AssignmentSubmit(models.Model):
    as_id=models.AutoField(primary_key=True)
    as_file=models.FileField(upload_to='submitassignments/')
    as_date=models.DateTimeField()
    as_marks=models.IntegerField(null=True,blank=True)
    as_plagiarismpercent=models.IntegerField(null=True,blank=True)
    as_assignmentid=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    as_studentid=models.ForeignKey(User,on_delete=models.CASCADE)



class QuizSubmit(models.Model):
    qs_id=models.AutoField(primary_key=True)
    qs_quizid=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    qs_questionid=models.ForeignKey(QuizQuestion,on_delete=models.CASCADE)
    qs_studentid=models.ForeignKey(User,on_delete=models.CASCADE)
    qs_answer=models.CharField(max_length=255)
    qs_obtmarks=models.IntegerField()
    qs_tmarks=models.IntegerField()
    qs_date=models.DateTimeField(null=True)

