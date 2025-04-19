from django.shortcuts import render
from accounts.models import Contest,Degree,Job
def home(request):
    user = request.user
    j=Job.objects.all()
    return render(request, 'home.html', {'user': user,'jobs':j})
def contests(request):
    c=Contest.objects.all()
    return render(request, 'contests.html',{'contests':c})
def degrees(request):
    d=Degree.objects.all()
    return render(request, 'degrees.html',{'degrees':d})
def career(request):
    return render(request,'career.html')
def privacy(request):
    return render(request,'privacy.html')
def support(request):
    v=request.GET.get('val')
    return render(request,'support.html',{'val':v})
def about(request):
    return render(request,'about.html')