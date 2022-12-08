from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import myAdminSignUpView,facultySignUpView,studentSignUpView

urlpatterns = [
    path("",views.index,name='index'),
    path("signin",views.signin,name='signin'),
    path("myadmin/home",views.adminhome,name='adminhome'),
    path("faculty/home",views.facultyhome,name='facultyhome'),
    path("student/home",views.studenthome,name='studenthome'),
    path('adminsignup', myAdminSignUpView.as_view(), name='myadmin_signup'),
    path('logout',views.logout_view,name='logout'),
    path('myadmin/profile',views.profile,name='adminprofile'),
    path('myadmin/profile/update',views.updateprofile,name='adminupdateprofile'),
    path('myadmin/profile/updateimage',views.updateprofileimage,name='adminprofileimage'),
    path('myadmin/profile/updatepass',views.updateprofilepass,name='adminupdateprofilepass'),
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
    path('myadmin/faculty',views.facultyshow,name='faculty'),
    path('myadmin/createfaculty', facultySignUpView.as_view(), name='createfaculty'),
    path('myadmin/updatefaculty/<int:id>',views.updatefaculty,name='updatefaculty'),
    path('myadmin/deletefaculty/<int:id>',views.deletefaculty,name='deletefaculty'),
    path('myadmin/student',views.studentshow,name='student'),
    path('myadmin/createstudent', studentSignUpView.as_view(), name='createstudent'),
    path('myadmin/updatestudent/<int:id>', views.updatestudent, name='updatestudent'),
    path('myadmin/deletestudent/<int:id>',views.deletestudent,name='deletestudent'),
    path('myadmin/bcf',views.bcfshow,name='bcf'),
    path('myadmin/createbcf',views.createbcf,name='createbcf'),
    path('myadmin/updatebcf/<int:id>',views.updatebcf,name='updatebcf'),
    path('myadmin/deletebcf/<int:id>',views.deletebcf,name='deletebcf'),
    path('inactive',views.inactive,name='inactive'),
    path('faculty/profile',views.facultyprofile,name='facultyprofile'),

    path('test',views.test,name='test'),
    path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)