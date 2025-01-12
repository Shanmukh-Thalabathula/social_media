from django.shortcuts import render
from .forms import UserRegistrationForm
# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
    else:
        form = UserRegistrationForm()
    return render(request,'posts/login_register.html',{'form':form})

def user_register(request):
    pass

def user_logout(request):
    pass