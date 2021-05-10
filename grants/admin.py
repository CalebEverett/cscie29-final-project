from django.contrib import admin

# Register your models here.

from .models import ApplicationQuestion, Assignment, ReviewQuestion, Application

admin.site.register(Application)
admin.site.register(ApplicationQuestion)
admin.site.register(ReviewQuestion)
admin.site.register(Assignment)
