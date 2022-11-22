from django.contrib import admin
from django.urls import path
from . import views
from .views import myAdminSignUpView

urlpatterns = [
    path("",views.index,name='index'),
    path("signin",views.signin,name='signin'),
    path("adminhome",views.adminhome,name='adminhome'),
    path('adminsignup', myAdminSignUpView.as_view(), name='myadmin_signup'),
    path('logout',views.logout_view,name='logout'),
    path('profile',views.profile,name='profile')
]