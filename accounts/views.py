from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages,auth
from accounts.models import CustomUser,JobPosting,UserProfile,Application
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
def seekprofile(request):
    i = request.GET.get('val')
    userobj = get_object_or_404(CustomUser, id=int(i))
    try:
        check = UserProfile.objects.get(user=userobj)
        context = {'info':check}  # If found, no additional context is needed
    except UserProfile.DoesNotExist:
        context = {'val': 1}  # Pass context when UserProfile is not found
    return render(request, 'seekrprofile.html', context)
def seekinfo(request):
    val1 = request.GET.get('val1')  # Flag to check profile creation
    val2 = request.GET.get('val2')  # CustomUser ID

    # Retrieve the CustomUser instance
    userobj = get_object_or_404(CustomUser, id=val2)

    if request.method == "POST":
        # Extract data from POST request
        about_me = request.POST.get('about_me', '')
        skills = request.POST.get('skills', '')
        work_experience = request.POST.get('work_experience', '')
        education = request.POST.get('education', '')
        projects = request.POST.get('projects', '')

        if val1:  # For creating a profile
            profile, created = UserProfile.objects.get_or_create(user=userobj)
            profile.about_me = about_me
            profile.skills = skills
            profile.work_experience = work_experience
            profile.education = education
            profile.projects = projects
            profile.save()
        else:  # For editing an existing profile
            profile = get_object_or_404(UserProfile, user=userobj)
            profile.about_me = about_me
            profile.skills = skills
            profile.work_experience = work_experience
            profile.education = education
            profile.projects = projects
            profile.save()

 
        return render(request, 'seekrprofile.html', {'info':profile})

    else:
        # For GET requests, check whether the profile exists
        if val1:
            profile, created = UserProfile.objects.get_or_create(user=userobj)
        else:
            profile = get_object_or_404(UserProfile, user=userobj)

        # Pass the profile data to the template for rendering
        context = {
            'user': userobj,
            'about_me': profile.about_me,
            'skills': profile.skills,
            'work_experience': profile.work_experience,
            'education': profile.education,
            'projects': profile.projects,
        }
        return render(request, 'seekinfo.html', context)
def logout(request):
    auth.logout(request)
    return redirect('/')
def applicants(request):
    job_id = request.GET.get('val2')  # job ID
    jobobj = get_object_or_404(Job, id=job_id)
    
    # Get all applications for this job
    applications = Application.objects.filter(job=jobobj).select_related('applicant')

    return render(request, 'applicants.html', {
        'applications': applications,
        'job': jobobj
    })
def login(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('/')  # Redirect to the home page or dashboard
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    return render(request, 'login.html')
def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        role = request.POST.get('role')
        emailid = request.POST.get('emailid')
        password = request.POST.get('password')
        phonenumber = request.POST.get('phonenumber')
        usename=request.POST.get('username')
        if not firstname or not emailid or not password or not phonenumber:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('/account/register')
        try:
            user = CustomUser.objects.create(
                first_name=firstname,
                last_name=lastname,
                role=role,
                email=emailid,
                password=make_password(password), 
                phone_number=phonenumber,
                username=usename 
            )
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('/account/login/')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('/account/register')

    return render(request, 'register.html')
def empprofile(request):
    return render(request,'empprofile.html')
def joblist(request):
    jobs = Job.objects.all()
    val = request.GET.get('val')
    v = request.GET.get('v')
    jt = request.GET.get('job_type')
    gn = request.GET.get('gender')
    if jt:
        j = Job.objects.filter(job_type=jt)
        return render(request, 'joblist.html', {'jobs': j})
    if gn:
        j = Job.objects.filter(gender=gn)
        return render(request, 'joblist.html', {'jobs': j})
    if val:
        user = get_object_or_404(CustomUser, id=val)
        posted = JobPosting.objects.filter(hiring_manager=user)
        myjobs = [post.job for post in posted]  # Extract jobs linked to JobPosting
        if v:
            return render(request, 'joblist.html', {'jobs': myjobs,'val':v})
        return render(request, 'joblist.html', {'jobs': myjobs})
    
    return render(request, 'joblist.html', {'jobs': jobs})
def jobdetails(request):
    val1=request.GET.get('val1')
    val2=request.GET.get('val2')
    val=request.GET.get('apply')
    jobs=get_object_or_404(Job,id=val2)
    if val:
        if val1=='None':
            return redirect('/account/login/')
        else:
            user=get_object_or_404(CustomUser,id=val1)
            application=Application.objects.create(job=jobs,applicant=user)
            application.save()
            return redirect('/')
    return render(request, 'jobdetails.html', {'job': jobs,'u':val1})
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Job

def postjob(request):
    if request.method == 'POST':
        val=request.GET.get('val')
        title = request.POST.get('title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        start_salary = request.POST.get('startsalary')
        end_salary = request.POST.get('endsalary')
        job_type = request.POST.get('job_type')
        gender = request.POST.get('gender')
        description = request.POST.get('description')

        # Validate form data (optional but recommended)
        if not title or not company_name or not location or not start_salary or not end_salary or not job_type or not gender or not description:
            messages.error(request, 'Please fill out all fields correctly.')
            return redirect('/accounts/postjob/')  # Replace 'post_job' with your URL name

        try:
            # Create a new job entry
            j = Job.objects.create(
                title=title,
                company_name=company_name,
                location=location,
                start_salary=start_salary,
                end_salary=end_salary,
                job_type=job_type,
                gender=gender,
                description=description
            )
            j.save()
            user=get_object_or_404(CustomUser,id=val)
            myjob=JobPosting.objects.create(hiring_manager=user,job=j)
            myjob.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('/account/postjob/') 
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('account/postjob/')  
    return render(request, 'postjob.html')  