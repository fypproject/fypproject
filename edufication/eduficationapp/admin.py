from django.contrib import admin

# Register your models here.
from .models import Student,Faculty,myAdmin,User
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(myAdmin)