from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.IndexPage,name="index"),
    path('signup/',views.SignUp,name="signup"),
    path('register/',views.RegisterUser,name="register"),
    path('otp/',views.OtpPage,name="otppage"),
    path('login/',views.LoginPage,name="login"),
    path('loginuser/',views.LoginUser,name="loginuser"),
    path('profile/',views.ProfilePage,name="profile"),
    path('updateProfile/',views.UpdateCandidateProfile,name="updateprofile"),
    path('updatePic/',views.UpdatePics,name="updatepic"),
    path('rollbackPic/',views.rollBackPics,name="rollbackpic"),
    
    path('logout/', views.logout_user, name='logout'),
    path('joblist/', views.JobList, name='joblist'),
    path('jobdetail/<int:id>/', views.JobDetail, name='jobdetail'),
    path('summit/<int:id>/', views.SummitApplication, name='summit'),
    path('apply/<int:id>/', views.apply, name='apply'),
    path('search', views.SearchResult, name='search'),
    path('Aboutus', views.Aboutus, name='aboutus'),
    
    
    
    # Company 
    
    
    path('company',views.CompanyPage,name="company"),
    path('company/profile',views.CompanyProfilePage,name="companyprofile"),
    path('company/updateprofile',views.UpdateCompanyProfile,name="updatecompanyprofile"),
    path('company/postjobpage',views.PostJobPage,name="postjobpage"),
    path('company/postjob',views.PostJob,name="postjob"),
    path('company/jobpostlist',views.JobPostlist,name="jobpostlist"),
    path('company/deletepost/<int:id>',views.deletePost,name="deletepost"),
    path('company/editpost/<int:id>',views.editPost,name="editpost"),
    path('company/applicationlist',views.ApplicationList,name="applicationlist"),
    path('company/jobpostlist/active/<int:id>',views.activejob,name="active"),
    path('company/jobpostlist/<int:id>',views.deactivatejob,name="deactivate"),
    
    
]

