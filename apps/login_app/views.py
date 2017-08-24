from django.shortcuts import render, redirect, HttpResponse
from models import User
from django.contrib import messages

def home(request):
	return redirect('/main')

def index(request):
	return render(request, "login_app/index.html")

def register(request):
	results = User.objects.regVal(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
		return redirect('/')
	user = User.objects.createUser(request.POST)
	request.session['userid'] = user.id
	request.session['name'] = user.name
	request.session['username'] = user.username
	messages.success(request, "User has been created. Please log in to continue.")
	return redirect('/main')

def login(request):
	results = User.objects.loginVal(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
			return redirect('/main')

	request.session['userid'] = results['user'].id
	request.session['name'] = results['user'].name
	request.session['username'] = results['user'].username
	return redirect('/dashboard')

def logout(request):
	request.session.flush()
	return redirect('/')
