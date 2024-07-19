from django.shortcuts import render,HttpResponse

# Create your views here.
def admin_home(request):
    return HttpResponse('This is admin home page')