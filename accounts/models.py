# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('hiring_manager', 'Hiring Manager'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self): 
        return self.username
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    about_me = models.TextField(blank=True, null=True)
    skills = models.TextField(help_text="Comma-separated skills", blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True) 
    education = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True) 
   
    def __str__(self):
        return f"{self.user.username}'s Profile"
class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
    ]
    GENDER_CHOICES = [
        ('Any', 'Any'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    image = models.ImageField(upload_to='job_images/', blank=True)
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_salary = models.IntegerField()
    end_salary = models.IntegerField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class JobPosting(models.Model):
    hiring_manager = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
class Application(models.Model): 
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    class Meta:
        unique_together = ('job', 'applicant')
class SavedJob(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
class Contest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    end_date = models.DateField()
    link = models.URLField()

    def __str__(self):
        return self.title
class Degree(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    join_link = models.URLField()

    def __str__(self):
        return self.title
