from django.shortcuts import render

# Create your views here.

def register_view(request):
    return render(request, 'account/register.html')

def login_view(request):
    return render(request, 'account/login.html')