from django.contrib import admin
from .models import Job, Application, JobPosting, Contest, Degree,SavedJob,CustomUser,UserProfile
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('first_name','last_name','username', 'email', 'role','password','phone_number', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone_number')}),
    )

admin.site.register(Job)
admin.site.register(Application)
admin.site.register(JobPosting)
admin.site.register(Contest)
admin.site.register(Degree)
admin.site.register(SavedJob)
admin.site.register(UserProfile)