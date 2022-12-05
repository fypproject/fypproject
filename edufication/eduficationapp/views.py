from xml.dom import ValidationErr
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.views.generic import CreateView            
from django.forms.utils import ErrorList

from .forms import myAdminSignUpForm,facultySignUpForm,studentSignUpForm
from .models import *
from django.views.decorators.cache import cache_control

# @cache_control(no_cache=True, must_revalidate=True)
# def func():
#     #some code
#     return redirect(index)


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    return render(request,"index.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    msg=''
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        print(username,password)
        user=authenticate(username=username,password=password)
        
        print(user)
        if user is not None:
            if user.is_student:
                student= Student.objects.get(user_id=user.id)
            elif user.is_faculty:
                faculty=Faculty.objects.get(user_id=user.id)
            elif user.is_myadmin:
                admin= myAdmin.objects.get(user_id=user.id)
            
            if user.is_authenticated and user.is_myadmin:
                #print(user.id,user.username)
                login(request, user)
                return redirect(adminhome)
            elif user.is_authenticated and user.is_faculty and faculty.f_status=="Active":
                login(request, user)
                return redirect(facultyhome)
            elif user.is_authenticated and user.is_faculty and faculty.f_status=="Inactive":
                return redirect(inactive)
            
            elif user.is_authenticated and user.is_student and student.s_status=="Active":
                login(request, user)
                return redirect(studenthome)
            
            elif user.is_authenticated and user.is_student and student.s_status=="Inactive":
                
                return redirect(inactive)
            else:
                return redirect(index)
        else:
            messages.error(request,"Invalid Username/Password")
            return render(request,"signin.html")
    return render(request,"signin.html")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    
    return redirect(index)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminhome(request):
    # myadmin=myAdmin.object.filter(user=request.user)
    batch= Batch.objects.all()
    course=Course.objects.all()
    bcf=Bcf.objects.all()
    student= User.objects.filter(is_student=True)
    faculty= User.objects.filter(is_faculty=True)
    program= Program.objects.all()
    user = request.user
    if user.is_authenticated and user.is_myadmin:
        context={'user':user,'userrole':"Admin",'batches':batch,'courses':course,'bcfs':bcf,'students':student,'faculties':faculty,'programs':program}
        #print(user.username) 
        return render(request,"adminhome.html",context)
    else:
        return redirect(index)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def facultyhome(request):
    # myadmin=myAdmin.object.filter(user=request.user)
    user = request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        context={'user':user,'userrole':"Faculty",'bcf':bcf}
        return render(request,"facultyhome.html",context)
    else:
        return redirect(index)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def studenthome(request):
    # myadmin=myAdmin.object.filter(user=request.user)
    user = request.user
   
    if user.is_authenticated and user.is_student:
        context={'user':user,'userrole':"Student"}
        return render(request,"facultyhome.html",context)
    else:
        return redirect(index)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    user=request.user
    if user.is_authenticated and user.is_myadmin:
        context={'user':user,'userrole':"Admin"}
        print(user.username) 
        return render(request,"profile.html",context)
    else:
        return redirect(index)
    

def updateprofile(request):
    user=request.user
    
    if user.is_authenticated and user.is_myadmin:
        if request.method == "POST":
            name= request.POST['txtfname']
            email=request.POST['txtemail']
            phone_no=request.POST['txtphoneno']
            city=request.POST['txtcity']
            country=request.POST['txtcountry']
            user.first_name=name
            user.email=email
            user.save()
            admin1=myAdmin.objects.get(user_id=user.id)
            admin1.ad_phoneno=phone_no
            admin1.ad_city=city
            admin1.ad_country=country
            admin1.save()
            return redirect(profile)


def updateprofileimage(request):
    user=request.user
    
    if user.is_authenticated and user.is_myadmin:
        if request.method == "POST":
            image= request.FILES['File']
            admin1= myAdmin.objects.get(user_id=user.id)
            admin1.ad_image=image
            admin1.save()
            return redirect(profile)
            
def updateprofilepass(request):
    user=request.user
    msg=""
    if user.is_authenticated and user.is_myadmin:
        if request.method == "POST":
            oldpass=request.POST['txtoldpass']
            newpass=request.POST['txtnewpass']
            if user.check_password(oldpass):
                user.set_password(newpass)
                user.save()
            else:
                msg="Wrong Old Password"

                return render(request,"profile.html",{'msg':msg,'userrole':"Admin"})
                print("Password Not Changed")
            return redirect(profile)





class myAdminSignUpView(CreateView):
    model = User
    form_class = myAdminSignUpForm
    template_name = 'adminsignup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'myAdmin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect(signin)


    
# Program Crud
def programshow(request):
    program= Program.objects.all()
    #print(program)
    return render(request,"program.html",{'programs':program,'userrole':"Admin"})


def createprogram(request):
    if request.method == "POST":
        programname= request.POST['programname']
        print(programname)
        program =Program(p_name=programname)
        program.save()
        return redirect(programshow)
    return render(request,"createprogram.html",{'userrole':"Admin"})

def updateprogram(request,id):
    program = Program.objects.get(p_id=id)
    print(program.p_name)
    if request.method == "POST":
        programname= request.POST['programname']
        program.p_name= programname
        program.save()
        return redirect(programshow)
        # program.p_name(programname)
        
    return render(request,"updateprogram.html",{'program':program,'userrole':"Admin"})

def deleteprogram(request,id):
    program = Program.objects.get(p_id=id)
    program.delete()
    return redirect(programshow)

# Batch Crud
def batchshow(request):
    batch= Batch.objects.all()
    #print(batch)
    
    return render(request,"batch.html",{'batchs':batch,'userrole':"Admin"})


def createbatch(request):
    program = Program.objects.all()
    if request.method == "POST":
        batchname= request.POST['batchname']
        programname =request.POST['program']
        programid= Program.objects.get(p_name=programname)
        print(programname)
        batch = Batch(b_name=batchname,b_programid=programid)
        
        #batch = Batch()
        # batch.b_name=batchname
        # batch.b_programid=program
        batch.save()
        return redirect(batchshow)
    return render(request,"createbatch.html",{'programs':program,'userrole':"Admin"})

def updatebatch(request,id):
    program = Program.objects.all()
    batch = Batch.objects.get(b_id=id)
    print(batch.b_name)
    if request.method == "POST":
        batchname= request.POST['batchname']
        programname=request.POST['program']
        batch.b_name= batchname
        batch.b_programid=Program.objects.get(p_name=programname)
        batch.save()
        return redirect(batchshow)
        # batch.p_name(batchname)
        
    return render(request,"updatebatch.html",{'batch':batch,'programs':program,'userrole':"Admin"})

def deletebatch(request,id):
    batch = Batch.objects.get(b_id=id)
    batch.delete()
    return redirect(batchshow)







# Course Crud
def courseshow(request):
    course= Course.objects.all()
    #print(course)
    
    return render(request,"course.html",{'courses':course,'userrole':"Admin"})


def createcourse(request):
    program = Program.objects.all()
    if request.method == "POST":
        coursename= request.POST['coursename']
        programname =request.POST['program']
        programid= Program.objects.get(p_name=programname)
        print(programname)
        course = Course(c_name=coursename,c_programid=programid)
        
        #course = course()
        # course.b_name=coursename
        # course.b_programid=program
        course.save()
        return redirect(courseshow)
    return render(request,"createcourse.html",{'programs':program,'userrole':"Admin"})

def updatecourse(request,id):
    program = Program.objects.all()
    course = Course.objects.get(c_id=id)
    print(course.c_name)
    if request.method == "POST":
        coursename= request.POST['coursename']
        programname=request.POST['program']
        course.c_name= coursename
        course.c_programid=Program.objects.get(p_name=programname)
        course.save()
        return redirect(courseshow)
        # course.p_name(coursename)
        
    return render(request,"updatecourse.html",{'course':course,'programs':program,'userrole':"Admin"})

def deletecourse(request,id):
    course = Course.objects.get(c_id=id)
    course.delete()
    return redirect(courseshow)

#faculty Crud

class facultySignUpView(CreateView):
    model = User
    form_class = facultySignUpForm
    template_name = 'createfaculty.html'
    userrole= "Admin"

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['userrole'] = self.userrole
        kwargs['user_type'] = 'faculty'
        return context

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect(facultyshow)

def facultyshow(request):
    faculty= User.objects.filter(is_faculty=True)
    #print(course)
    
    return render(request,"faculty.html",{'faculties':faculty,'userrole':"Admin"})

def updatefaculty(request,id):
    faculty=User.objects.get(id=id)
    faculty1= Faculty.objects.get(user_id=id)
    context={'faculty':faculty,'userrole':"Admin"}
    if request.method =="POST":
        statusname=request.POST['txtstatus']
        faculty1.f_status=statusname
        faculty1.save()
        return redirect(facultyshow)
    return render(request,"updatefaculty.html",context)
def deletefaculty(request,id):
    faculty = User.objects.get(id=id)
    faculty.delete()
    return redirect(facultyshow)

# Student Crud

class studentSignUpView(CreateView):
    model = User
    form_class = studentSignUpForm
    template_name = 'createstudent.html'
    userrole= "Admin"

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['userrole'] = self.userrole
        kwargs['user_type'] = 'student'
        return context

    def form_valid(self, form):
        
        #s_batchid = form.cleaned_data.get('s_batchid')
        
        #form.save(commit=False)
        user= form.save()
        # user= Student(s_batchid=s_batchid)
        # user.save()
        
        
        
        #login(self.request, user)
        return redirect(studentshow)
        # self.object = form.save(commit=False)
        # self.object.user = self.request.user

        # try:
        #     self.object.full_clean()
        # except ValidationErr:
        #     #raise ValidationError("No can do, you have used this name before!")
        #     #return self.form_invalid(form)
        #     form._errors["s_regno"] = ErrorList([u"Registration number already exists..."])
        #     return super(studentSignUpView, self).form_invalid(form)

        return super(studentSignUpView, self).form_valid(form),redirect(studentshow)
def studentshow(request):
    student= User.objects.filter(is_student=True)
    #print(course)
    
    return render(request,"student.html",{'students':student,'userrole':"Admin"})

def updatestudent(request,id):
    student=User.objects.get(id=id)
    student1= Student.objects.get(user_id=id)
    batch = Batch.objects.all()
    context={'student':student,'batches':batch,'userrole':"Admin"}
    if request.method =="POST":
        batchname= request.POST['txtbatch']
        statusname=request.POST['txtstatus']
        batchid=Batch.objects.get(b_name=batchname)
        student1.s_batchid=batchid
        student1.s_status=statusname
        student1.save()
        return redirect(studentshow)



    return render(request,"updatestudent.html",context)

def deletestudent(request,id):
    student = User.objects.get(id=id)
    student.delete()
    return redirect(studentshow)

# Batch Faculty Crud
def bcfshow(request):
    bcf= Bcf.objects.all()
    return render(request,"bcf.html",{'userrole':"Admin",'bcfs':bcf})

def createbcf(request):
    faculty= User.objects.filter(is_faculty=True)
    batch=Batch.objects.all()
    course = Course.objects.all()
    context={'courses':course,'faculties':faculty,'batches':batch,'userrole':"Admin"}
    if request.method == "POST":
        coursename= request.POST['txtcourse']
        facultyname =request.POST['txtfaculty']
        batchname=request.POST['txtbatch']
        courseid= Course.objects.get(c_name=coursename)
        batchid=Batch.objects.get(b_name=batchname)
        facultyid=User.objects.get(username=facultyname)
        
        #print(programname)
        bcf = Bcf(bcf_batchid=batchid,bcf_courseid=courseid,bcf_facultyid=facultyid)
        bcf.save()
        return redirect(bcfshow)
    return render(request,"createbcf.html",context)

def updatebcf(request,id):
    course = Course.objects.all()
    faculty= User.objects.filter(is_faculty=True)
    batch=Batch.objects.all()
    bcf = Bcf.objects.get(bcf_id=id)
    context={'courses':course,'faculties':faculty,'batches':batch,'userrole':"Admin",'bcf':bcf}
    if request.method == "POST":
        coursename= request.POST['txtcourse']
        facultyname =request.POST['txtfaculty']
        batchname=request.POST['txtbatch']
        bcf.bcf_courseid= Course.objects.get(c_name=coursename)
        bcf.bcf_batchid=Batch.objects.get(b_name=batchname)
        bcf.bcf_facultyid=User.objects.get(username=facultyname)
        
        #print(programname)
        bcf.save()
        return redirect(bcfshow)
    
    # print(course.c_name)
    # if request.method == "POST":
    #     coursename= request.POST['coursename']
    #     programname=request.POST['program']
    #     course.c_name= coursename
    #     course.c_programid=Program.objects.get(p_name=programname)
    #     course.save()
    #     return redirect(courseshow)
    #     # course.p_name(coursename)
        
    return render(request,"updatebcf.html",context)
    
def deletebcf(request,id):
    bcf = Bcf.objects.get(bcf_id=id)
    bcf.delete()
    return redirect(bcfshow)


def inactive(request):
    return render(request,"inactive.html")


def test(request):
    batch=Batch.objects.all()
    context={'batches':batch}
    return render(request,"test.html",context)

def load_courses(request):
    batchid = request.GET.get('batch')
    print(batchid)
    batch= Batch.objects.get(b_name=batchid)
    print(batch.b_programid)
    courses = Course.objects.filter(c_programid=batch.b_programid)
    
    return render(request, 'loadcoursesdropdown.html',{'courses':courses})
