from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.views.generic import CreateView
from .forms import myAdminSignUpForm
from .models import User,Student,myAdmin
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
                return redirect(adminhome)
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
def adminhome(request):
    # myadmin=myAdmin.object.filter(user=request.user)
    user = request.user
    if user.is_authenticated and user.is_myadmin:
        context={'user':user,'userrole':"Admin"}
        print(user.username) 
        return render(request,"adminhome.html",context)
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