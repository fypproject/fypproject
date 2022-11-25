from django.contrib import admin
from django.urls import path
from . import views
from .views import myAdminSignUpView

urlpatterns = [
    path("",views.index,name='index'),
    path("signin",views.signin,name='signin'),
    path("myadmin/home",views.adminhome,name='adminhome'),
    path('adminsignup', myAdminSignUpView.as_view(), name='myadmin_signup'),
    path('logout',views.logout_view,name='logout'),
    path('myadmin/profile',views.profile,name='adminprofile'),
    path('myadmin/createprogram',views.createprogram,name='createprogram'),
    path('myadmin/program',views.programshow,name='program'),
    path('myadmin/updateprogram/<int:id>',views.updateprogram,name='updateprogram'),
    path('myadmin/deleteprogram/<int:id>',views.deleteprogram,name='deleteprogram'),
    path('myadmin/createbatch',views.createbatch,name='createbatch'),
    path('myadmin/batch',views.batchshow,name='batch'),
    path('myadmin/updatebatch/<int:id>',views.updatebatch,name='updatebatch'),
    path('myadmin/deletebatch/<int:id>',views.deletebatch,name='deletebatch'),
    path('myadmin/createcourse',views.createcourse,name='createcourse'),
    path('myadmin/course',views.courseshow,name='course'),
    path('myadmin/updatecourse/<int:id>',views.updatecourse,name='updatecourse'),
    path('myadmin/deletecourse/<int:id>',views.deletecourse,name='deletecourse'),
]