from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(myAdmin)
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(Bcf)
admin.site.register(Lecture)
admin.site.register(Assignment)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(Attendance)
admin.site.register(AttendanceRecord)
admin.site.register(AssignmentSubmit)
admin.site.register(QuizSubmit)