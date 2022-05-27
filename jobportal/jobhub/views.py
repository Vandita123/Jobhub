from datetime import date
from django.contrib.auth import *
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from .helpers import *

#jobseeker signup
def jobseeker_signup(request):
    if request.method == 'POST':#if it's post method
        #fetching values from html
        f = request.POST.get('firstName')
        l = request.POST.get('lastName')
        contact = request.POST.get('mobile')
        g = request.POST.get('gender')
        birth = request.POST.get('dob')
        mail = request.POST.get('email')
        p = request.POST.get('password')
        cp = request.POST.get('cpass')
        s = request.POST.get('state')
        ct = request.POST.get('city')
        a = request.POST.get('address')
        exp = request.POST.get('experience')
        ed = request.POST.get('education')
        sk = request.POST.get('skills')
        if p != cp:
            messages.success(request, 'Password and Conform Password are not same.')
            return redirect('/recruiter_signup')
        try:
            if User.objects.filter(username=mail).first(): #if user with same email exist
                messages.success(request, 'Email has been taken is taken.')
                return redirect('/jobseeker_signup')
            user = User.objects.create_user(username=mail, password=p)
            auth_token = str(uuid.uuid4()) #create a token for email verification
            data = jobseeker(user=user, J_fname=f, auth_token=auth_token, J_lname=l, J_email=mail, J_password=p, J_contact=contact, J_address=a, J_city=ct, J_experience=exp, J_state=s, J_dob=birth, J_gender=g, J_education=ed, J_skill=sk, type="student")
            data.save() #save all the data into databaase
            send_mail_after_registration(mail, auth_token) #send mail to user's email
            return redirect('/token')
        except Exception as e:
            print(e)
    return render(request, 'jobseeker_signup.html')

def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')

#verify jobseeker account
def verify(request, auth_token):
    try:
        profile_obj = jobseeker.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified: #if account already verified
                messages.success(request, 'Your account is already verified.')
                return redirect('/jobseeker_login')
            profile_obj.is_verified = True #make account verified
            profile_obj.save() #save value to database
            messages.success(request, 'Your account has been verified.')
            return redirect('/jobseeker_login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
    return redirect('/')

def error_page(request):
    return render(request, 'error.html')

#send mail for email verification to jobseeker
def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def recruiter_signup(request):
    if request.method == 'POST':
        #fetching values from html
        n = request.POST.get('cname')
        c = request.POST.get('mobile')
        e = request.POST.get('email')
        pw = request.POST.get('pass')
        cpw = request.POST.get('cpass')
        a = request.POST.get('address')
        w = request.POST.get('website')
        d = request.POST.get('description')
        if pw != cpw:
            messages.success(request, 'Password and Conform Password are not same.')
            return redirect('/recruiter_signup')
        try:
            if User.objects.filter(username=e).first():#if email already exist
                messages.success(request, 'Email has been taken is taken.')
                return redirect('/recruiter_signup')

            user = User.objects.create_user(username=e, password=pw)
            auth_token = str(uuid.uuid4()) #generate token for email verification
            data = jobprovider(user=user, U_name=n, U_email=e, U_password=pw,auth_token=auth_token, U_contact=c,
                                   U_address=a, U_website=w, U_about=d, type="recruiter")
            data.save() #saving values to database
            send_mail_after_reg(e, auth_token) #sending email for verification
            return redirect('/token')
        except Exception as e:
            print(e)
    return render(request, 'recruiter_signup.html')

#verify jobprovider account
def verify_j(request, auth_token):
    try:
        profile_obj = jobprovider.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified: #if account already verified
                messages.success(request, 'Your account is already verified.')
                return redirect('/recruiter_login')
            profile_obj.is_verified = True #make account verified
            profile_obj.save() #save value to database
            messages.success(request, 'Your account has been verified.')
            return redirect('/recruiter_login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
    return redirect('/')

#send mail for email verification to jobprovider
def send_mail_after_reg(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify_j/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def jobseeker_login(request):
    error=""
    if request.method == 'POST':
        #fetching values from html
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None: #if user's email doesn't exist
            messages.success(request, 'User not found.')
            return redirect('/jobseeker_login')
        profile_obj = jobseeker.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified: #if email is now verified
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/jobseeker_login')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/jobseeker_login')
        login(request, user)
        error="no"
    d = {'error': error}
    return render(request, 'jobseeker_login.html',d)

def recruiter_login(request):
    error = ""
    if request.method == "POST":
        # fetching values from html
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None: #if user's email doesn't exist
            messages.success(request, 'User not found.')
            return redirect('/recruiter_login')
        profile_obj = jobprovider.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified: #if email is now verified
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/recruiter_login')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/recruiter_login')
        login(request, user)
        error = "no"
    d = {'error': error}
    return render(request, "recruiter_login.html",d)

def ChangePassword(request, token):
    context = {}
    try:
        jobseeker_obj = jobseeker.objects.filter(forget_password_token=token).first()
        context = {'username': jobseeker_obj.user.username}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            username = request.POST.get('username')
            if username is None:
                messages.success(request, 'No user found.')
                return redirect(f'/change-password/{token}/')
            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
            user_obj = User.objects.get(username=username)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/jobseeker_login/')
    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)

import uuid

def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'No user found with this username.')
                return redirect('/forget-password/')
            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            jobseeker_obj = jobseeker.objects.get(user=user_obj)
            jobseeker_obj.forget_password_token = token
            jobseeker_obj.save()
            send_forget_password_mail(user_obj.username, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')

def ForgetPassword_J(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.success(request, 'No user found with this username.')
                return redirect('/forget-password-j/')
            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            jobprovider_obj = jobprovider.objects.get(user=user_obj)
            jobprovider_obj.forget_password_token = token
            jobprovider_obj.save()
            send_forget_passwordj_mail(user_obj.username, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password-j/')
    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')

def ChangePassword_J(request, token):
    context = {}
    try:
        jobprovider_obj = jobprovider.objects.filter(forget_password_token=token).first()
        context = {'username': jobprovider_obj.user.username}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            username = request.POST.get('username')
            if username is None:
                messages.success(request, 'No user found.')
                return redirect(f'/change-password-j/{token}/')
            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password-j/{token}/')
            user_obj = User.objects.get(username=username)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/recruiter_login/')
    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)

def jobseeker_home(request):
    if not request.user.is_authenticated:
        return redirect('jobseeker_login')
    user = request.user
    student = jobseeker.objects.get(user=user)
    error = ""
    if request.method == "POST":
        c = request.POST.get('contact')
        add = request.POST.get('address')
        st = request.POST.get('state')
        ct = request.POST.get('city')
        ex = request.POST.get('experience')
        ed = request.POST.get('education')
        sk = request.POST.get('skill')

        student.J_contact = c
        student.J_address = add
        student.J_state = st
        student.J_city = ct
        student.J_experience = ex
        student.J_education = ed
        student.J_skill = sk

        try:
            student.save()
            student.user.save()
            error = "no"
        except:
            error = "yes"
    d = {'student': student, 'error': error}
    return render(request, "jobseeker_home.html", d)

def jobprovider_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = jobprovider.objects.get(user=user)
    error = ""
    if request.method == "POST":
        cont = request.POST.get('contact')
        ad = request.POST.get('address')
        ab = request.POST.get('about')

        recruiter.U_contact = cont
        recruiter.U_address = ad
        recruiter.U_about = ab
        try:
            recruiter.save()
            recruiter.user.save()
            error = "no"
        except:
            error = "yes"

    d = {'recruiter': recruiter, 'error': error}
    return render(request, 'jobprovider_home.html', d)

def submit_review(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    try:
        if request.method == 'POST':
            rate = request.POST.get('rating')
            r = request.POST.get('review')
            user = request.user
            try:
                ReviewRating.objects.create(rating=rate, review=r, create_date=date.today(),email=user.username)
                error = "no"
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    d = {'error': error}
    return render(request, 'reviewtest.html', d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == 'POST':
        t = request.POST.get('title')
        c = request.POST.get('contact')
        a = request.POST.get('address')
        sd = request.POST.get('startdate')
        ed = request.POST.get('enddate')
        s = request.POST.get('salary')
        ex = request.POST.get('experience')
        sk = request.POST.get('skills')
        ab = request.POST.get('about')
        role = request.POST.get('role')
        if sd > ed:
            messages.success(request, 'Start date is greater the end date.')
            return redirect('/add_job')
        user = request.user
        recruiter = jobprovider.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter, title=t, contact=c, location=a, start_date=sd, end_date=ed,
                               salary=s, experience=ex, skills=sk, about=ab,role=role, creationdate=date.today())
            error = "no"
            subject = 'New job update'
            user = request.user
            job = Job.objects.get(id=user.id)
            d = {'job': job, 'id': user.id}
            message = render_to_string('job_notification.html', d)
            plain_message = strip_tags(message)
            email_from = settings.EMAIL_HOST_USER
            student = jobseeker.objects.all()
            jobseeker_list = []
            for i in student:
                jobseeker_list.append(i.user.username)
            send_mail(subject, plain_message, email_from, jobseeker_list)
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_job.html', d)

def edit_job(request, pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=pid)
    if request.method == 'POST':
        c = request.POST.get('contact')
        a = request.POST.get('address')
        sd = request.POST.get('startdate')
        ed = request.POST.get('enddate')
        s = request.POST.get('salary')
        ex = request.POST.get('experience')
        sk = request.POST.get('skills')
        ab = request.POST.get('about')

        job.U_contact = c
        job.location = a
        job.salary = s
        job.experience = ex
        job.skills = sk
        job.about = ab
        try:
            job.save()
            error = "no"
        except:
            error = "yes"

        if sd:
            try:
                job.start_date = sd
                job.save()
            except:
                pass
        else:
            pass

        if ed:
            try:
                job.end_date = ed
                job.save()
            except:
                pass
        else:
            pass
    d = {'error': error, 'job': job}
    return render(request, 'edit_job.html', d)

def job_search(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('jobseeker_login')
    job = Job.objects.all().order_by('-start_date')
    user = request.user
    student = jobseeker.objects.get(user=user)
    data = apply.objects.filter(student=student)
    if request.method == "POST":
        f1 = request.POST.get('f1')
        f2 = request.POST.get('f2')
        try:
            for i in job:
                j = Job.objects.get(id=i.id)
                j.filter1 = f1
                j.filter2 = f2
                j.save()
            error = "no"
        except Exception as e:
            print(e)
    else:
        try:
            for i in job:
                j = Job.objects.get(id=i.id)
                j.filter1 = "Interested Field"
                j.filter2 = "Location"
                j.save()
        except Exception as e:
            print(e)
    li = []
    for i in data:
        li.append(i.job.id)
    d = {'job': job, 'li': li, 'error':error}
    return render(request, 'job_search.html', d)

def job_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('jobseeker_login')
    job = Job.objects.get(id=pid)
    d = {'job': job, 'id': pid}
    return render(request, 'job_detail.html', d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = jobprovider.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    d = {'job': job}
    return render(request, 'job_list.html', d)

def applicant(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    data = apply.objects.all()
    d = {'data': data}
    return render(request, 'applicant.html', d)

def download(request, pid):
    if not request.user.is_authenticated:
        return redirect('jobseeker_login')
    obj = apply.objects.get(id=pid)
    filename = obj.resume.path
    response = FileResponse(open(filename, 'rb'))
    return response

def job_apply(request, pid):
    if not request.user.is_authenticated:
        return redirect('jobseeker_login')
    error = ""
    user = request.user
    student = jobseeker.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1 = date.today()
    if job.end_date < date1:
        error = "close"
    elif job.start_date > date1:
        error = "notopen"
    else:
        if request.method == "POST":
            r = request.FILES['resume']
            apply.objects.create(job=job, student=student, resume=r, applydate=date.today())
            error = "no"
    d = {'error': error,'student':student}
    return render(request, 'job_apply.html', d)

def Logout(request):
    logout(request)
    return redirect('jobseeker_login')

def logout_jobprovider(request):
    logout(request)
    return redirect('recruiter_login')

def home(request):
    job = Job.objects.all().order_by('-start_date')
    feedback = ReviewRating.objects.all().order_by('-create_date')
    d = {'job': job, 'feedback': feedback}
    return render(request, 'home.html', d)


def latest_joblist(request):
    job = Job.objects.all().order_by('-start_date')
    d = {'job': job}
    return render(request, 'latest_joblist.html', d)


def delete_job(request, pid):
    if not request.user.is_authenticated:
        return redirect('jobprovider_login')
    job = Job.objects.get(id=pid)
    job.delete()
    return redirect('job_list')
