from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import *




@login_required(login_url='login')
def home_page(request):
    My_title="hello World...."
    My_list=[1,2,3,4,5]
    if request.user.is_authenticated:
        context={"title":My_title, "List":My_list}
    else:
        context={"title":My_title}
    return render(request, "home.html", context)
    
@login_required(login_url='login')
def contact_page(request):
    form = contactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = contactForm()

    template_name = 'contact.html'
    context = {
        "title" : "Contact Us",
        "form" : form
    }
    return render(request, template_name, context)

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'register.html', context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')










