from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.views.generic import CreateView
from .forms import myAdminSignUpForm,facultySignUpForm
from .models import User,Student,myAdmin,Program,Batch,Course
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

    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        print(username,password)
        user=authenticate(username=username,password=password)
        print(user)
        if user is not None:
            
            login(request, user)
            if user.is_authenticated and user.is_myadmin:
                #print(user.id,user.username)
                return redirect(home)
            elif user.is_authenticated and user.is_faculty:
                return redirect(home)
            else:
                return redirect(index)
        else:
            print(password,username)
    return render(request,"signin.html")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    
    return redirect(index)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    # myadmin=myAdmin.object.filter(user=request.user)
    user = request.user
    if user.is_authenticated and user.is_myadmin:
        context={'user':user,'userrole':"Admin"}
        #print(user.username) 
        return render(request,"adminhome.html",context)
    elif user.is_authenticated and user.is_faculty:
        context={'user':user,'userrole':"Faculty"}
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

class facultySignUpView(CreateView):
    model = User
    form_class = facultySignUpForm
    template_name = 'facultysignup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'faculty'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect(signin)
    
# Program Crud
def programshow(request):
    program= Program.objects.all()
    print(program)
    return render(request,"program.html",{'programs':program})


def createprogram(request):
    if request.method == "POST":
        programname= request.POST['programname']
        print(programname)
        program =Program(p_name=programname)
        program.save()
        return redirect(programshow)
    return render(request,"createprogram.html")

def updateprogram(request,id):
    program = Program.objects.get(p_id=id)
    print(program.p_name)
    if request.method == "POST":
        programname= request.POST['programname']
        program.p_name= programname
        program.save()
        return redirect(programshow)
        # program.p_name(programname)
        
    return render(request,"updateprogram.html",{'program':program})

def deleteprogram(request,id):
    program = Program.objects.get(p_id=id)
    program.delete()
    return redirect(programshow)

# Batch Crud
def batchshow(request):
    batch= Batch.objects.all()
    #print(batch)
    
    return render(request,"batch.html",{'batchs':batch})


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
    return render(request,"createbatch.html",{'programs':program})

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
        
    return render(request,"updatebatch.html",{'batch':batch,'programs':program})

def deletebatch(request,id):
    batch = Batch.objects.get(b_id=id)
    batch.delete()
    return redirect(batchshow)







# Course Crud
def courseshow(request):
    course= Course.objects.all()
    #print(course)
    
    return render(request,"course.html",{'courses':course})


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
    return render(request,"createcourse.html",{'programs':program})

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
        
    return render(request,"updatecourse.html",{'course':course,'programs':program})

def deletecourse(request,id):
    course = Course.objects.get(c_id=id)
    course.delete()
    return redirect(courseshow)


