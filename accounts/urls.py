from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('seekprofile/', views.seekprofile),
    path('empprofile/', views.empprofile),
    path('login/', views.login),
    path('applicants/', views.applicants),
    path('logout/', views.logout),
    path('register/', views.register),
    path('job/', views.joblist),
    path('seekinfo/',views.seekinfo),
    path('postjob/',views.postjob),
    path('jobdetails/', views.jobdetails),
]