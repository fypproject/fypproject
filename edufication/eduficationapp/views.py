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



### Faculty Section


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
           
                
            
            
    return render(request,"updatelecture.html",context)
def deletelecture(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        lecture = Lecture.objects.get(l_id=id)
        lecture.delete()
        return redirect(lecturehome,id=lecture.l_bcfid.bcf_id)





### Assignment Scenes 
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

def createassignment(request,id):
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
            txtmark=request.POST['txtmark']
            file=request.FILES.get('File')
            assignment1= Assignment(a_name=txtchoice,a_desc=txtdesc,a_startdate=stdate,a_enddate=enddate,a_mark=txtmark,a_file=file,a_bcfid=bcfid)
            assignment1.save()
            return redirect(assignmenthome,id=bcfid.bcf_id)
            

    else:
        return redirect(index)
    return render(request,"createassignment.html",context)

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
           
                
            
            
    return render(request,"updateassignment.html",context)
def deleteassignment(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        assignment = Assignment.objects.get(a_id=id)
        assignment.delete()
        return redirect(assignmenthome,id=assignment.a_bcfid.bcf_id)


### Quiz Scenes

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
            question=request.POST['question']
            quiz1= Quiz(q_name=txtname,q_startdate=stdate,q_enddate=enddate,q_question=question,q_bcfid=bcfid)
            quiz1.save()
            #print(quiz1.q_id)
            return redirect(createqquiz,id=quiz1.q_id)
            
            

    else:
        return redirect(index)
    return render(request,"createquiz.html",context)

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
            
            quiz.q_startdate=stdate
            quiz.q_enddate=enddate
            quiz.save()
                
            
            #print(assignment.l_bcfid.bcf_id)
            return redirect(quizhome,id=quiz.q_bcfid.bcf_id)    
           
                
            
            
    return render(request,"updatequiz.html",context)
def deletequiz(request,id):
    user=request.user
    if user.is_authenticated and user.is_faculty:
        quiz = Quiz.objects.get(q_id=id)
        quiz.delete()
        return redirect(quizhome,id=quiz.q_bcfid.bcf_id)


### Quiz Questions Scenes

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



            # for i in range(qquiz,quiz.q_question):
            #     qquiz1=QuizQuestion(qq_question=question,qq_option1=opt1,qq_option2=opt2,qq_option3=opt3,qq_option4=opt4,qq_marks=mark,qq_correctanswer=ans,qq_quizid=quiz)
            #     qquiz1.save()
            #     if qquiz == quiz.q_question-1:
            #         return redirect(quizhome,id=quiz.q_bcfid.bcf_id)
            #     return redirect(createqquiz,id=quiz.q_id)
            #return redirect(quizhome,id=quiz.q_bcfid.bcf_id)
    return render(request,"createqquiz.html",context)


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

    
    return render(request,"createattendancerecord.html",context)



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
