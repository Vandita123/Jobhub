from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(jobseeker)
admin.site.register(jobprovider)
admin.site.register(Job)
admin.site.register(apply)
admin.site.register(ReviewRating)