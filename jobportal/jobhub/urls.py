"""
   ALL URL FOR JOBHUB CREATED INSIDE urls.py FILE
"""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('latest_joblist/', views.latest_joblist, name="latest_joblist"),

    path('forget-password/', views.ForgetPassword, name="forget_password"),
    path('change-password/<token>/', views.ChangePassword, name="change_password"),

    path('forget-password-j/', views.ForgetPassword_J, name="forget_password"),
    path('change-password-j/<token>/', views.ChangePassword_J, name="change_password"),

    path('jobseeker_login/', views.jobseeker_login, name="jobseeker_login"),
    path('recruiter_login/', views.recruiter_login, name="recruiter_login"),

    path('jobseeker_signup/', views.jobseeker_signup, name="jobseeker_signup"),
    path('recruiter_signup/', views.recruiter_signup, name="recruiter_signup"),

    path('jobseeker_home/', views.jobseeker_home, name="jobseeker_home"),
    path('job_search/', views.job_search, name="job_search"),
    path('job_apply/<int:pid>/', views.job_apply, name="job_apply"),
    path('job_detail/<int:pid>/', views.job_detail, name="job_detail"),
    path('Logout/', views.Logout, name="Logout"),

    path('jobprovider_home/', views.jobprovider_home, name="jobprovider_home"),
    path('add_job/', views.add_job, name="add_job"),
    path('job_list/', views.job_list, name="job_list"),
    path('edit_job/<int:pid>/', views.edit_job, name="edit_job"),
    path('delete_job/<int:pid>/', views.delete_job, name="delete_job"),
    path('applicant/', views.applicant, name="applicant"),
    path('download/<int:pid>/', views.download, name="download"),
    path('logout_jobprovider/', views.logout_jobprovider, name="logout_jobprovider"),

    path('submit_review/', views.submit_review, name='submit_review'),

    path('token', views.token_send , name="token_send"),#generated to verify account
    path('success', views.success , name='success'),
    path('verify/<auth_token>', views.verify , name="verify"),#to verify account
    path('verify_j/<auth_token>', views.verify_j , name="verify"),
    path('error', views.error_page , name="error")

] + static(settings.IMAGES_URL, document_root=settings.IMAGES_ROOT)
