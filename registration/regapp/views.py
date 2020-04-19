from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserProfileForm, UserForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.


def base(request):
    return render(request, 'base.html')


def index(request):
    return render(request, 'index.html')


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        userprofile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            userprofile = userprofile_form.save(commit=False)
            userprofile.user = user

            if 'profile_pic' in request.FILES:
                userprofile.profile_pic = request.FILES['profile_pic']

            userprofile.save()
            registered = True

        else:
            print(user_form.errors, userprofile_form.errors)

    else:
        user_form = UserForm()
        userprofile_form = UserProfileForm()

    return render(request, 'registration.html', {'user_form':user_form, 'userprofile_form':userprofile_form, 'registered':registered})

def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse("User cannot be authenticated!")
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request,'login.html')