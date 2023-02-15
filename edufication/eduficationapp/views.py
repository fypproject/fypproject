from xml.dom import ValidationErr
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.views.generic import CreateView            
from django.forms.utils import ErrorList
from datetime import datetime

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
        bcf=Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        #print(bcf)
        context={'user':user,'userrole':"Student",'bcf':bcf}
        return render(request,"studenthome.html",context)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def facultyprofile(request):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        context={'user':user,'userrole':"Faculty",'bcf':bcf}
        print(user.username) 
        return render(request,"facultyprofile.html",context)
    else:
        return redirect(index)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def studentprofile(request):
    user=request.user
    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        context={'user':user,'userrole':"Student",'bcf':bcf}
        print(user.username) 
        return render(request,"studentprofile.html",context)
    else:
        return redirect(index)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
    elif user.is_authenticated and user.is_faculty:
        if request.method == "POST":
            name= request.POST['txtfname']
            email=request.POST['txtemail']
            phone_no=request.POST['txtphoneno']
            city=request.POST['txtcity']
            country=request.POST['txtcountry']
            qualifications=request.POST['txtqualifications']
            user.first_name=name
            user.email=email
            user.save()
            faculty1=Faculty.objects.get(user_id=user.id)
            faculty1.f_phoneno=phone_no
            faculty1.f_city=city
            faculty1.f_country=country
            faculty1.f_qualifications=qualifications

            faculty1.save()
            return redirect(facultyprofile)
    elif user.is_authenticated and user.is_student:
        if request.method == "POST":
            name= request.POST['txtfname']
            email=request.POST['txtemail']
            phone_no=request.POST['txtphoneno']
            city=request.POST['txtcity']
            country=request.POST['txtcountry']
            parentscontact=request.POST['txtparentscontact']
            user.first_name=name
            user.email=email
            user.save()
            student1=Student.objects.get(user_id=user.id)
            student1.s_phoneno=phone_no
            student1.s_city=city
            student1.s_country=country
            student1.s_parentscontact=parentscontact

            student1.save()
            return redirect(studentprofile)  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateprofileimage(request):
    user=request.user
    
    if user.is_authenticated and user.is_myadmin:
        if request.method == "POST":
            image= request.FILES['File']
            admin1= myAdmin.objects.get(user_id=user.id)
            admin1.ad_image=image
            admin1.save()
            return redirect(profile)
    elif user.is_authenticated and user.is_faculty:
        if request.method == "POST":
            image= request.FILES['File']
            faculty1= Faculty.objects.get(user_id=user.id)
            faculty1.f_image=image
            faculty1.save()
            return redirect(facultyprofile)
    elif user.is_authenticated and user.is_student:
        if request.method == "POST":
            image= request.FILES['File']
            student1= Student.objects.get(user_id=user.id)
            student1.s_image=image
            student1.save()
            return redirect(studentprofile)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)           
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
    elif user.is_authenticated and user.is_faculty:
        if request.method == "POST":
            oldpass=request.POST['txtoldpass']
            newpass=request.POST['txtnewpass']
            if user.check_password(oldpass):
                user.set_password(newpass)
                user.save()
            else:
                msg="Wrong Old Password"

                return render(request,"facultyprofile.html",{'msg':msg,'userrole':"Faculty"})
                print("Password Not Changed")
            return redirect(facultyprofile)
    elif user.is_authenticated and user.is_student:
        if request.method == "POST":
            oldpass=request.POST['txtoldpass']
            newpass=request.POST['txtnewpass']
            if user.check_password(oldpass):
                user.set_password(newpass)
                user.save()
            else:
                msg="Wrong Old Password"

                return render(request,"studentprofile.html",{'msg':msg,'userrole':"Student"})
                print("Password Not Changed")
            return redirect(studentprofile)



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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def programshow(request):
    program= Program.objects.all()
    #print(program)
    return render(request,"program.html",{'programs':program,'userrole':"Admin"})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createprogram(request):
    if request.method == "POST":
        programname= request.POST['programname']
        print(programname)
        program =Program(p_name=programname)
        program.save()
        return redirect(programshow)
    return render(request,"createprogram.html",{'userrole':"Admin"})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteprogram(request,id):
    program = Program.objects.get(p_id=id)
    program.delete()
    return redirect(programshow)

# Batch Crud
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def batchshow(request):
    batch= Batch.objects.all()
    programbatch=Program.objects.all()
    #print(batch)
    
    return render(request,"batch.html",{'batchs':batch,'userrole':"Admin",'programs':programbatch})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletebatch(request,id):
    batch = Batch.objects.get(b_id=id)
    batch.delete()
    return redirect(batchshow)







# Course Crud
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def courseshow(request):
    course= Course.objects.all()
    #print(course)
    program=Program.objects.all()
    return render(request,"course.html",{'courses':course,'userrole':"Admin",'programs':program})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def facultyshow(request):
    faculty= User.objects.filter(is_faculty=True)
    #print(course)
    
    return render(request,"faculty.html",{'faculties':faculty,'userrole':"Admin"})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def studentshow(request):
    student= User.objects.filter(is_student=True)
    batch=Batch.objects.all()
    #print(course)
    
    return render(request,"student.html",{'students':student,'userrole':"Admin",'batches':batch})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletestudent(request,id):
    student = User.objects.get(id=id)
    student.delete()
    return redirect(studentshow)

# Batch Faculty Crud

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bcfshow(request):
    bcf= Bcf.objects.all()
    return render(request,"bcf.html",{'userrole':"Admin",'bcfs':bcf})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createbcf(request):
    msg=""
    faculty= User.objects.filter(is_faculty=True)
    batch=Batch.objects.all()
    bcfobject=Bcf.objects.all()
    course = Course.objects.all()
    
    if request.method == "POST":
        coursename= request.POST['courses']
        facultyname =request.POST['txtfaculty']
        batchname=request.POST['batch']
        courseid= Course.objects.get(c_name=coursename)
        batchid=Batch.objects.get(b_name=batchname)
        facultyid=User.objects.get(username=facultyname)
        for bcf1 in bcfobject:
            if bcf1.bcf_batchid == batchid and bcf1.bcf_courseid == courseid:
                #print("Course Already Assigned")
                msg="Course Already Assigned to this batch."
                return render(request,"createbcf.html",{'courses':course,'faculties':faculty,'batches':batch,'userrole':"Admin",'msg':msg})
            
                
        bcf = Bcf(bcf_batchid=batchid,bcf_courseid=courseid,bcf_facultyid=facultyid)
        #print("Saved")       
        bcf.save()    
        #print(programname)
        
        return redirect(bcfshow)
    context={'courses':course,'faculties':faculty,'batches':batch,'userrole':"Admin",'msg':msg}
    
    return render(request,"createbcf.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def deletebcf(request,id):
    bcf = Bcf.objects.get(bcf_id=id)
    bcf.delete()
    return redirect(bcfshow)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inactive(request):
    return render(request,"inactive.html")



### Faculty Section

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def coursegallery(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        #bcf1=Bcf.objects.get(bcf_facultyid=user.id,bcf_id=bcfid.bcf_id)
        if bcfid.bcf_facultyid is not None:
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf}
        else:
            return redirect(facultyhome)
    else:
        return redirect(index)
    return render(request,"coursegallery.html",context)

### Lecture Scenes

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def lecturehome(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        if bcfid.bcf_facultyid is not None:
            lecture= Lecture.objects.filter(l_bcfid=bcfid)
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'lectures':lecture}
        else:
            return redirect(facultyhome)
        
    else:
        return redirect(index)
    return render(request,"lecture.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createlecture(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        if bcfid.bcf_facultyid is not None:
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf}
        else:
            return redirect(facultyhome)
       
        if request.method == "POST":
            txtchoice= request.POST['txtchoice']
            txtdesc=request.POST['txtdesc']
            file=request.FILES.get('File')
            lecture1= Lecture(l_name=txtchoice,l_desc=txtdesc,l_file=file,l_bcfid=bcfid)
            lecture1.save()
            return redirect(lecturehome,id=bcfid.bcf_id)
            

    else:
        return redirect(index)
    return render(request,"createlecture.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updatelecture(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)

        #bcfid = Bcf.objects.get(bcf_id=id)
        lecture=Lecture.objects.get(l_id=id)
        context={'userrole':"Faculty",'bcf':bcf,'lecture':lecture}
        if request.method == "POST":
            txtdesc=request.POST['txtdesc']
            
            file=request.FILES.get('File')
            if file is None:
                lecture.l_desc=txtdesc
                lecture.save()
                
            else:
                lecture.l_desc=txtdesc
                lecture.l_file=file
                lecture.save()
            #print(lecture.l_bcfid.bcf_id)
            return redirect(lecturehome,id=lecture.l_bcfid.bcf_id)    
           
    else:
        return redirect(index)        
            
            
    return render(request,"updatelecture.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def deletelecture(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        lecture = Lecture.objects.get(l_id=id)
        lecture.delete()
        return redirect(lecturehome,id=lecture.l_bcfid.bcf_id)
    




### Assignment Scenes

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def assignmenthome(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        if bcfid.bcf_facultyid is not None :
            assignment= Assignment.objects.filter(a_bcfid=bcfid)
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'assignments':assignment}
        else:
            return redirect(facultyhome)
        
    else:
        return redirect(index)
    return render(request,"assignment.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createassignment(request,id):
    msg=""
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        if bcfid.bcf_facultyid is not None:
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf}
        else:
            return redirect(facultyhome)
        
        if request.method == "POST":
            txtchoice= request.POST['txtname']
            txtdesc=request.POST['txtdesc']
            stdate=request.POST['stdate']
            enddate=request.POST['enddate']
            now=datetime.now()
            date_time = now.strftime("%Y-%m-%dT%H:%M")
            if stdate <= date_time:
                msg="Wrong Start date and time"
                return render(request,"createassignment.html",{'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'msg':msg})
            if stdate > enddate:
                msg="Wrong End date and time"
                #print(datetime.now())
                return render(request,"createassignment.html",{'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'msg':msg})
            

            
            txtmark=request.POST['txtmark']
            file=request.FILES.get('File')
            assignment1= Assignment(a_name=txtchoice,a_desc=txtdesc,a_startdate=stdate,a_enddate=enddate,a_mark=txtmark,a_file=file,a_bcfid=bcfid)
            assignment1.save()
            return redirect(assignmenthome,id=bcfid.bcf_id)
            

    else:
        return redirect(index)
    return render(request,"createassignment.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateassignment(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)

        #bcfid = Bcf.objects.get(bcf_id=id)
        assignment=Assignment.objects.get(a_id=id)
        context={'userrole':"Faculty",'bcf':bcf,'assignment':assignment}
        if request.method == "POST":
            txtdesc=request.POST['txtdesc']
            stdate=request.POST['stdate']
            enddate=request.POST['enddate']
            now=datetime.now()
            date_time = now.strftime("%Y-%m-%dT%H:%M")
            if stdate <= date_time:
                msg="Wrong Start date and time"
                return render(request,"updateassignment.html",{'userrole':"Faculty",'assignment':assignment,'bcf':bcf,'msg':msg})
            if stdate > enddate:
                msg="Wrong End date and time"
                #print(datetime.now())
                return render(request,"updateassignment.html",{'userrole':"Faculty",'assignment':assignment,'bcf':bcf,'msg':msg})
            txtmark=request.POST['txtmark']
            file=request.FILES.get('File')
            if file is None:
                assignment.a_desc=txtdesc
                assignment.a_startdate=stdate
                assignment.a_enddate=enddate
                assignment.a_mark=txtmark
                assignment.save()
                
            else:
                assignment.a_desc=txtdesc
                assignment.a_startdate=stdate
                assignment.a_enddate=enddate
                assignment.a_mark=txtmark
                assignment.a_file=file
                assignment.save()
            #print(assignment.l_bcfid.bcf_id)
            return redirect(assignmenthome,id=assignment.a_bcfid.bcf_id)    
           
    else:
        return redirect(index)             
            
            
    return render(request,"updateassignment.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteassignment(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        assignment = Assignment.objects.get(a_id=id)
        assignment.delete()
        return redirect(assignmenthome,id=assignment.a_bcfid.bcf_id)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def receivedassignment(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        assignment= Assignment.objects.get(a_id=id)

        try:
            bcfid = Bcf.objects.get(bcf_id=assignment.a_bcfid.bcf_id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        studentsarr=[]
        assubmitarr=[]
        if bcfid.bcf_facultyid is not None :
            user1=User.objects.filter(is_student=True)
            
            for student in user1:
                student1=Student.objects.filter(user=student,s_batchid=bcfid.bcf_batchid.b_id)

                if student1.exists():
                    #print(student1)
                    studentsarr.append(student1[0])
                    assignmentsubmit=AssignmentSubmit.objects.filter(as_assignmentid=assignment.a_id,as_studentid=student)
                    if assignmentsubmit.exists():
                        assubmitarr.append(assignmentsubmit[0])
                        #print(assignmentsubmit[0])
                    else:
                        assubmitarr.append('')


            #print(assubmitarr)
            assignmentreceived=list(zip(studentsarr,assubmitarr))
            #student1=Student.objects.filter(user=User.objects.filter(is_student=True),s_batchid=bcfid.bcf_batchid.b_id)
            # print(student1)
            #print(studentsarr[0])
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'assignments':assignment,'assignmentreceived':assignmentreceived}
        else:
            return redirect(facultyhome)
        
    else:
        return redirect(index)
    return render(request,"receivedassignment.html",context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateassignmentmarks(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        assignmentsubmit=AssignmentSubmit.objects.get(as_id=id)
        assignment= Assignment.objects.get(a_id=assignmentsubmit.as_assignmentid.a_id)

        try:

            bcfid = Bcf.objects.get(bcf_id=assignment.a_bcfid.bcf_id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        if bcfid.bcf_facultyid is not None :
            
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'assignmentsubmit':assignmentsubmit}
        else:
            return redirect(facultyhome)
        
        if request.method== "POST":
            marks=request.POST["marks"]
            assignmentsubmit.as_marks=marks
            assignmentsubmit.save()
            return redirect(receivedassignment,id=assignmentsubmit.as_assignmentid.a_id)
        
    else:
        return redirect(index)
    return render(request,"updateassignmentmarks.html",context)



### Quiz Scenes
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def quizhome(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        if bcfid.bcf_facultyid is not None:
            quiz= Quiz.objects.filter(q_bcfid=bcfid)
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'quizes':quiz}
        else:
            return redirect(facultyhome)
        
    else:
        return redirect(index)
    return render(request,"quiz.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createquiz(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        if bcfid.bcf_facultyid is not None:
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf}
        else:
            return redirect(facultyhome)
        if request.method == "POST":
            txtname= request.POST['txtname']
            stdate=request.POST['stdate']
            enddate=request.POST['enddate']
            now=datetime.now()
            date_time = now.strftime("%Y-%m-%dT%H:%M")
            if stdate <= date_time:
                msg="Wrong Start date and time"
                return render(request,"createquiz.html",{'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'msg':msg})
            if stdate > enddate:
                msg="Wrong End date and time"
                #print(datetime.now())
                return render(request,"createquiz.html",{'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'msg':msg})
            question=request.POST['question']
            quiz1= Quiz(q_name=txtname,q_startdate=stdate,q_enddate=enddate,q_question=question,q_bcfid=bcfid)
            quiz1.save()
            #print(quiz1.q_id)
            return redirect(createqquiz,id=quiz1.q_id)
            
            

    else:
        return redirect(index)
    return render(request,"createquiz.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updatequiz(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)

        #bcfid = Bcf.objects.get(bcf_id=id)
        quiz=Quiz.objects.get(q_id=id)
        context={'userrole':"Faculty",'bcf':bcf,'quiz':quiz}
        if request.method == "POST":
            stdate=request.POST['stdate']
            enddate=request.POST['enddate']
            now=datetime.now()
            date_time = now.strftime("%Y-%m-%dT%H:%M")
            if stdate <= date_time:
                msg="Wrong Start date and time"
                return render(request,"updatequiz.html",{'userrole':"Faculty",'bcf':bcf,'quiz':quiz,'msg':msg})
            if stdate > enddate:
                msg="Wrong End date and time"
                #print(datetime.now())
                return render(request,"updatequiz.html",{'userrole':"Faculty",'bcf':bcf,'quiz':quiz,'msg':msg})
            quiz.q_startdate=stdate
            quiz.q_enddate=enddate
            quiz.save()
                
            
            #print(assignment.l_bcfid.bcf_id)
            return redirect(quizhome,id=quiz.q_bcfid.bcf_id)    
           
    else:
        return redirect(index)            
            
            
    return render(request,"updatequiz.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletequiz(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        quiz = Quiz.objects.get(q_id=id)
        quiz.delete()
        return redirect(quizhome,id=quiz.q_bcfid.bcf_id)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def receivedquiz(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        quiz= Quiz.objects.get(q_id=id)

        try:
            bcfid = Bcf.objects.get(bcf_id=quiz.q_bcfid.bcf_id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        studentsarr=[]
        qssubmitarr=[]
        obtmarks=[]
        if bcfid.bcf_facultyid is not None :
            quizquestion=QuizQuestion.objects.filter(qq_quizid=quiz.q_id)
            total=0
            for qq in quizquestion:
                total=total+qq.qq_marks
            user1=User.objects.filter(is_student=True)
            
            for student in user1:
                student1=Student.objects.filter(user=student,s_batchid=bcfid.bcf_batchid.b_id)

                if student1.exists():
                    #print(student1)
                    studentsarr.append(student1[0])
                    quizsubmit=QuizSubmit.objects.filter(qs_quizid=quiz.q_id,qs_studentid=student)
                    
                    obt=0
                    
                    if quizsubmit.exists():
                        qssubmitarr.append(quizsubmit[0])
                        for qs in quizsubmit:
                            
                            obt=obt+qs.qs_obtmarks
                        
                    else:
                        qssubmitarr.append('')

                    #print(obt)
                    obtmarks.append(obt)
                    
            
            quizreceived=list(zip(studentsarr,qssubmitarr,obtmarks))
            #student1=Student.objects.filter(user=User.objects.filter(is_student=True),s_batchid=bcfid.bcf_batchid.b_id)
            # print(student1)
            #print(studentsarr[0])
            
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'quizzes':quiz,'quizreceived':quizreceived,'totalmarks':total}
        else:
            return redirect(facultyhome)
        
    else:
        return redirect(index)
    return render(request,"receivedquiz.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewquiz(request,id,pk):
    user=request.user
    

    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        quiz= Quiz.objects.get(q_id=id)

        try:
            bcfid = Bcf.objects.get(bcf_id=quiz.q_bcfid.bcf_id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        
        #quizquestion=QuizQuestion.objects.filter(qq_quizid=quiz.q_id)
        quizsubmit=QuizSubmit.objects.filter(qs_quizid=quiz.q_id,qs_studentid=pk)
        studentrecord=QuizSubmit.objects.filter(qs_quizid=quiz.q_id,qs_studentid=pk).first()
        print(studentrecord)
        total=0
        obt=0
        for qs in quizsubmit:
            total=total+qs.qs_tmarks
            obt=obt+qs.qs_obtmarks
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'quiz':quiz,'quizsubmit':quizsubmit,'totalmarks':total,'obtmarks':obt,'studentrecord':studentrecord}
        else:
            return redirect(facultyhome)
        
        
            

    else:
        return redirect(index)
    return render(request,"viewquiz.html",context)



### Quiz Questions Scenes

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createqquiz(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        quiz=Quiz.objects.get(q_id=id)
        qquiz=QuizQuestion.objects.filter(qq_quizid=quiz.q_id).count()
        context={'userrole':"Faculty",'bcf':bcf}
        if request.method == "POST":
            question= request.POST['txtques']
            opt1=request.POST['opt1']
            opt2=request.POST['opt2']
            opt3=request.POST['opt3']
            opt4=request.POST['opt4']
            mark=request.POST['mark']
            ans=request.POST['ans']
            qquiz1=QuizQuestion(qq_question=question,qq_option1=opt1,qq_option2=opt2,qq_option3=opt3,qq_option4=opt4,qq_marks=mark,qq_correctanswer=ans,qq_quizid=quiz)
            qquiz1.save()
            if qquiz == quiz.q_question-1:
                return redirect(quizhome,id=quiz.q_bcfid.bcf_id)
            
            return redirect(createqquiz,id=quiz.q_id)

    else:
        return redirect(index) 

            # for i in range(qquiz,quiz.q_question):
            #     qquiz1=QuizQuestion(qq_question=question,qq_option1=opt1,qq_option2=opt2,qq_option3=opt3,qq_option4=opt4,qq_marks=mark,qq_correctanswer=ans,qq_quizid=quiz)
            #     qquiz1.save()
            #     if qquiz == quiz.q_question-1:
            #         return redirect(quizhome,id=quiz.q_bcfid.bcf_id)
            #     return redirect(createqquiz,id=quiz.q_id)
            #return redirect(quizhome,id=quiz.q_bcfid.bcf_id)
    return render(request,"createqquiz.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def qquizhome(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        
        try:
            quizid= Quiz.objects.get(q_id=id)    
            bcfid=Bcf.objects.get(bcf_id=quizid.q_bcfid.bcf_id,bcf_facultyid=user.id)
        except:
            
            return redirect(facultyhome)
        if bcfid is not None:
            quiz=Quiz.objects.get(q_id=quizid.q_id)
            qquiz1= QuizQuestion.objects.filter(qq_quizid=quizid)
            context={'userrole':"Faculty",'bcf':bcf,'qquizes':qquiz1,'quiz':quiz}
        else:
            return redirect(facultyhome)
        
        
    else:
        return redirect(index)

    return render(request,"qquiz.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateqquiz(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        
        
        #quiz=Quiz.objects.get(q_id=id)
        qquiz1= QuizQuestion.objects.get(qq_id=id)
        context={'userrole':"Faculty",'bcf':bcf,'qquiz':qquiz1}  

        if request.method == "POST":
            question= request.POST['txtques']
            opt1=request.POST['opt1']
            opt2=request.POST['opt2']
            opt3=request.POST['opt3']
            opt4=request.POST['opt4']
            mark=request.POST['mark']
            ans=request.POST['ans']
            qquiz1.qq_question=question
            qquiz1.qq_option1=opt1
            qquiz1.qq_option2=opt2
            qquiz1.qq_option3=opt3
            qquiz1.qq_option4=opt4
            qquiz1.qq_marks=mark
            qquiz1.qq_correctanswer=ans
            qquiz1.save()
            return redirect(qquizhome,id=qquiz1.qq_quizid.q_id)  
    else:
        return redirect(index)

    return render(request,"updateqquiz.html",context)



### Attendance Scenes

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attendancehome(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        if bcfid.bcf_facultyid is not None:
            attendance= Attendance.objects.filter(at_bcfid=bcfid)
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf,'attendances':attendance}
        else:
            return redirect(facultyhome)
        
    else:
        return redirect(index)
    return render(request,"attendance.html",context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createattendance(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_facultyid=user.id)
        except:
            return redirect(facultyhome)
        if bcfid.bcf_facultyid is not None:
            context={'bcfid':bcfid,'userrole':"Faculty",'bcf':bcf}
        else:
            return redirect(facultyhome)
        if request.method == "POST":
            txtname= request.POST['txtname']
            date=request.POST['date']
            attendance1= Attendance(at_name=txtname,at_date=date,at_bcfid=bcfid)
            attendance1.save()
            #print(quiz1.q_id)
            return redirect(createattendancerecord,id=attendance1.at_id)
            
            

    else:
        return redirect(index)
    return render(request,"createattendance.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createattendancerecord(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        attendance=Attendance.objects.get(at_id=id)
        bcfid=Bcf.objects.get(bcf_id=attendance.at_bcfid.bcf_id)

        studentuser=User.objects.filter(is_student=True)
        student=Student.objects.filter(s_batchid=bcfid.bcf_batchid)
        print(student.count())

        context={'userrole':"Faculty",'bcf':bcf,'students':student}
        if request.method == "POST":
            #print(request.POST)
            options=request.POST.getlist('txtoption')
            names=request.POST.getlist('txtname')
            # for name in names:
            #     print(name)
            
            # for option in options:
            #     print(option)
            for name,option in zip(names,options):
                print(name,option)
                
                attendancerecord=AttendanceRecord(atr_studentid=User.objects.get(first_name=name),atr_option=option,atr_atid=attendance)
                attendancerecord.save()
            return redirect(attendancehome,id=bcfid.bcf_id)    
    else:
        return redirect(index) 
    
    return render(request,"createattendancerecord.html",context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attendancerecordhome(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        
        try:
            attendanceid= Attendance.objects.get(at_id=id)    
            bcfid=Bcf.objects.get(bcf_id=attendanceid.at_bcfid.bcf_id,bcf_facultyid=user.id)
        except:
            
            return redirect(facultyhome)
        if bcfid is not None:
            attendance=Attendance.objects.get(at_id=attendanceid.at_id)
            attendancerecord= AttendanceRecord.objects.filter(atr_atid=attendanceid)
            context={'userrole':"Faculty",'bcf':bcf,'attendancerecord':attendancerecord,'attendance':attendance}
        else:
            return redirect(facultyhome)
        
        
    else:
        return redirect(index)


    return render(request,"attendancerecord.html",context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateattendancerecord(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        bcf= Bcf.objects.filter(bcf_facultyid=user.id)
        
        
        #quiz=Quiz.objects.get(q_id=id)
        attendancerecord1= AttendanceRecord.objects.get(atr_id=id)
        context={'userrole':"Faculty",'bcf':bcf,'attendancerecord':attendancerecord1}  

        if request.method == "POST":
            txtname= request.POST['txtname']
            txtoption=request.POST['txtoption']
            attendancerecord1.atr_option=txtoption
            attendancerecord1.save()
            return redirect(attendancerecordhome,id=attendancerecord1.atr_atid.at_id)  
    else:
        return redirect(index)

    return render(request,"updateattendancerecord.html",context)





### Students Scene


### Student Course Gallery
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def scoursegallery(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        try:
            bcfid = Bcf.objects.get(bcf_id=id,bcf_batchid=user.student.s_batchid)
        except:
            return redirect(studenthome)
        #bcf1=Bcf.objects.get(bcf_facultyid=user.id,bcf_id=bcfid.bcf_id)
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Student",'bcf':bcf}
        else:
            return redirect(studenthome)
    else:
        return redirect(index)
    return render(request,"scoursegallery.html",context)

### Student Attendance Home

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sattendancehome(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        atrecords=[]
        #print(attendancerecord1)
        try:
            
            bcfid = Bcf.objects.get(bcf_id=id,bcf_batchid=user.student.s_batchid)
            attendances=Attendance.objects.filter(at_bcfid=bcfid.bcf_id)
            for attendance in attendances:
                #print(attendance.at_id)
                attendancerecord1=AttendanceRecord.objects.get(atr_studentid=user.id,atr_atid=attendance.at_id)
                print(attendancerecord1)
                atrecords.append(attendancerecord1)
                    
            
        except:
            return redirect(studenthome)
        #studentname=attendancerecord1.atr_studentid
        #print(studentname)
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Student",'bcf':bcf,'atrecords':atrecords}
        else:
            return redirect(studenthome)
    else:
        return redirect(index)
    return render(request,"sattendance.html",context)


### Student Lecture Home
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def slecturehome(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        
        #print(attendancerecord1)
        try:
            
            bcfid = Bcf.objects.get(bcf_id=id,bcf_batchid=user.student.s_batchid)
            lecture=Lecture.objects.filter(l_bcfid=bcfid.bcf_id)
                    
            
        except:
            return redirect(studenthome)
        
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Student",'bcf':bcf,'lectures':lecture}
        else:
            return redirect(studenthome)
    else:
        return redirect(index)
    return render(request,"slecture.html",context)

### Student Assignment Scene

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sassignmenthome(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        arrenddate=[]
        arrsubdate=[]
        arrstartdate=[]
        assignmentsarr=[]
        #print(attendancerecord1)
        
        try:
            
            bcfid = Bcf.objects.get(bcf_id=id,bcf_batchid=user.student.s_batchid)
            

        except:
            return redirect(studenthome)
        assignment= Assignment.objects.filter(a_bcfid=bcfid.bcf_id)                    
        for ass in assignment:
            
            assignmentsubmit=AssignmentSubmit.objects.filter(as_assignmentid=ass.a_id,as_studentid=user.id)
            if assignmentsubmit.count() == 0:
                assignmentsarr.append('')
                arrsubdate.append('')
            else:
                for asse in assignmentsubmit:
                    assignmentsarr.append(asse)
                    arrsubdate.append(asse.as_date.strftime("%Y-%m-%d %H:%M"))

           
            
            arrenddate.append(ass.a_enddate.strftime("%Y-%m-%d %H:%M"))
            arrstartdate.append(ass.a_startdate.strftime("%Y-%m-%d %H:%M"))
        print(assignmentsarr)
        now=datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M")
        #print(date_time)
        
        assignment1=list(zip(assignment,arrenddate,assignmentsarr,arrsubdate,arrstartdate))
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Student",'bcf':bcf,'assignments':assignment1,'date_time':date_time}
        else:
            return redirect(studenthome)
    else:
        return redirect(index)
    return render(request,"sassignment.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submitassignment(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        assignment= Assignment.objects.get(a_id=id)  
        #print(attendancerecord1)
        try:
            
            bcfid = Bcf.objects.get(bcf_id=assignment.a_bcfid.bcf_id,bcf_batchid=user.student.s_batchid)   
                              

        except:
            return redirect(studenthome)
        
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Student",'bcf':bcf,'assignment':assignment}
        else:
            return redirect(studenthome)

        if request.method=="POST":
            file=request.FILES.get('File')
            assignmentsubmit=AssignmentSubmit(as_file=file,as_date=datetime.now(),as_assignmentid=assignment,as_studentid=User.objects.get(username=user.username))
            assignmentsubmit.save()
            return redirect(sassignmenthome,id=assignment.a_bcfid.bcf_id)
    else:
        return redirect(index)
    return render(request,"submitassignment.html",context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submittedassignment(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        assignment= Assignment.objects.get(a_id=id) 
        
        
        enddate=assignment.a_enddate.strftime("%Y-%m-%d %H:%M")
         
        
        now=datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M")
        #print(attendancerecord1)
        try:
            
            bcfid = Bcf.objects.get(bcf_id=assignment.a_bcfid.bcf_id,bcf_batchid=user.student.s_batchid)   
            assignmentsubmit=AssignmentSubmit.objects.get(as_assignmentid=id,as_studentid=user.id) 

        except:
            return redirect(studenthome)
        
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Student",'bcf':bcf,'assignment':assignment,'assignmentsubmit':assignmentsubmit,'enddate':enddate,'datetime':date_time}
        else:
            return redirect(studenthome)

        if request.method=="POST":
            file=request.FILES.get('File')
            assignmentsubmit.as_file=file
            assignmentsubmit.as_date=now
            assignmentsubmit.save()
            return redirect(sassignmenthome,id=assignment.a_bcfid.bcf_id)
    else:
        return redirect(index)
    return render(request,"submittedassignment.html",context)




### Student Quiz Scenes


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def squizhome(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        arrenddate=[]
        arrstartdate=[]
        arrsubdate=[]
        quizarr=[]
        #print(attendancerecord1)
        
        try:
            
            bcfid = Bcf.objects.get(bcf_id=id,bcf_batchid=user.student.s_batchid)
            

        except:
            return redirect(studenthome)
        quizs= Quiz.objects.filter(q_bcfid=bcfid.bcf_id)                    
        for quiz in quizs:
            quizsubmit=QuizSubmit.objects.filter(qs_quizid=quiz.q_id,qs_studentid=user.id)
            if quizsubmit.count() == 0:
                quizarr.append('')
                arrsubdate.append('')
            else:
                for quz in quizsubmit:
                    quizarr.append(quz)
                    arrsubdate.append(quz.qs_date.strftime("%Y-%m-%d %H:%M"))
            arrenddate.append(quiz.q_enddate.strftime("%Y-%m-%d %H:%M"))
            arrstartdate.append(quiz.q_startdate.strftime("%Y-%m-%d %H:%M"))
        now=datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M")
        quiz1=list(zip(quizs,arrenddate,quizarr,arrsubdate,arrstartdate))
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Student",'bcf':bcf,'quizzes':quiz1,'date_time':date_time}
        else:
            return redirect(studenthome)
    else:
        return redirect(index)
    return render(request,"squiz.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submitquiz(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        quiz= Quiz.objects.get(q_id=id)  
        quizquestion=QuizQuestion.objects.filter(qq_quizid=quiz.q_id)
        quizsubmitobj=QuizSubmit.objects.filter(qs_quizid=quiz.q_id,qs_studentid=user.id)
        enddate=quiz.q_enddate.strftime("%Y-%m-%d %H:%M")  
        now= datetime.now().strftime("%Y-%m-%d %H:%M")
        if enddate < now:
            return redirect(squizhome,id=quiz.q_bcfid.bcf_id)
        if quizsubmitobj.count()>0:
            return redirect(squizhome,id=quiz.q_bcfid.bcf_id)
        #print(quizquestion)
        #print(attendancerecord1)
        try:
            
            bcfid = Bcf.objects.get(bcf_id=quiz.q_bcfid.bcf_id,bcf_batchid=user.student.s_batchid)   
                              

        except:
            return redirect(studenthome)
        
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Student",'bcf':bcf,'quiz':quiz,'quizquestions':quizquestion}
        else:
            return redirect(studenthome)
        answersarr=[]
        if request.method=="POST":
            # option0=request.POST['option0']
            # option1=request.POST['option1']
            # option2=request.POST['option2']
            items=list(request.POST.items())
            for item in items:
                if 'question' in item[0]:
                    #print(item[1])
                    answersarr.append(item[1])
            
            #print(answersarr)
            quizsubmit=list(zip(answersarr,quizquestion))
            for answer,qq in quizsubmit:
                
                print(answer,qq)
                quizqid=QuizQuestion.objects.get(qq_id=qq.qq_id)
                if qq.qq_correctanswer == answer:

                    quizsubmitt=QuizSubmit(qs_quizid=quiz,qs_questionid=quizqid,qs_studentid=User.objects.get(username=user.username),qs_answer=answer,qs_obtmarks=qq.qq_marks,qs_tmarks=qq.qq_marks,qs_date=datetime.now())
                    print("True",)
                    
                else:
                    quizsubmitt=QuizSubmit(qs_quizid=quiz,qs_questionid=quizqid,qs_studentid=User.objects.get(username=user.username),qs_answer=answer,qs_obtmarks=0,qs_tmarks=qq.qq_marks,qs_date=datetime.now())
                    print("False")
                quizsubmitt.save()
            

            return redirect(squizhome,id=quiz.q_bcfid.bcf_id)
    else:
        return redirect(index)
    return render(request,"submitquiz.html",context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submittedquiz(request,id):
    user=request.user
    

    if user.is_authenticated and user.is_student:
        bcf= Bcf.objects.filter(bcf_batchid=user.student.s_batchid)
        quiz= Quiz.objects.get(q_id=id)
        enddate=quiz.q_enddate.strftime("%Y-%m-%d %H:%M")  
        now= datetime.now().strftime("%Y-%m-%d %H:%M")
        if enddate > now:
            return redirect(squizhome,id=quiz.q_bcfid.bcf_id)
        #quizquestion=QuizQuestion.objects.filter(qq_quizid=quiz.q_id)
        quizsubmit=QuizSubmit.objects.filter(qs_quizid=quiz.q_id,qs_studentid=user.id)
        try:
            
            bcfid = Bcf.objects.get(bcf_id=quiz.q_bcfid.bcf_id,bcf_batchid=user.student.s_batchid)   
                              

        except:
            return redirect(studenthome)
        total=0
        obt=0
        for qs in quizsubmit:
            total=total+qs.qs_tmarks
            obt=obt+qs.qs_obtmarks
        if bcfid.bcf_batchid is not None:
            context={'bcfid':bcfid,'userrole':"Student",'bcf':bcf,'quiz':quiz,'quizsubmit':quizsubmit,'totalmarks':total,'obtmarks':obt}
        else:
            return redirect(studenthome)
        
        
            

    else:
        return redirect(index)
    return render(request,"submittedquiz.html",context)



















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
