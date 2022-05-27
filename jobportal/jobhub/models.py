"""
   THE MODELS REQUIRED FOR JOBHUB CREATED INSIDE models.py FILE
"""
from django.db import models
from django.contrib.auth.models import User

class jobseeker(models.Model):
    J_email = models.CharField(primary_key=True,max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    J_fname = models.CharField(max_length=20)
    J_lname = models.CharField(max_length=20,null=True)
    J_address = models.CharField(max_length=50)
    J_city = models.CharField(max_length=15)
    J_experience = models.CharField(max_length=15)
    J_state = models.CharField(max_length=15)
    J_dob = models.CharField(max_length=10)
    J_gender = models.CharField(max_length=10)
    J_contact = models.CharField(max_length=10)
    J_password = models.CharField(max_length=50)
    J_education = models.CharField(max_length=20)
    J_skill = models.TextField(max_length=100,null=True)
    forget_password_token = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=100, default="", editable=False)
    is_verified = models.BooleanField(default=False)
    type = models.CharField(max_length=10)
    def _str_(self):
        return self.user.username

class jobprovider(models.Model):
    U_email = models.CharField(primary_key=True,max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    U_name = models.CharField(max_length=20)
    U_address = models.CharField(max_length=50)
    U_contact = models.CharField(max_length=10)
    U_password = models.CharField(max_length=50)
    U_website = models.CharField(max_length=20,null=True)
    U_about = models.TextField(max_length=100,null=True)
    forget_password_token = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=100, default="", editable=False)
    is_verified = models.BooleanField(default=False)
    type = models.CharField(max_length=10)
    def _str_(self):
        return self.user.username

class Job(models.Model):
    recruiter = models.ForeignKey(jobprovider, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    contact = models.TextField(max_length=10)
    experience = models.CharField(max_length=100)
    salary = models.FloatField(max_length=20)
    filter1 = models.CharField(default="Interested Field", max_length=20)
    filter2 = models.CharField(default="Location", max_length=20)
    skills = models.TextField(max_length=100)
    role = models.TextField(max_length=100)
    about = models.TextField(max_length=100, null=True)
    creationdate = models.DateField()
    def _str_(self):
        return self.title

class apply(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(jobseeker, on_delete=models.CASCADE)
    resume = models.FileField()
    applydate = models.DateField()
    def _str_(self):
        return self.id


class ReviewRating(models.Model):
    email = models.CharField(max_length=500)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(default=5)
    create_date = models.DateTimeField(auto_now_add=True)
    def str(self):
        return self.id
