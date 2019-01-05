
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.urls import reverse

def index(request):
    return render(request, "default/index.html")

def register(request):
	if request.method == "POST":
		errors = User.objects.isValidRegistration(request.POST)
		if len(errors) < 1:
			for key,value in errors.items():
				messages.error(request, value)
			if User.objects.filter(email = request.POST['email']):
				hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
				User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed)
				request.session['name'] = request.POST['first_name']
				request.session['logged_in'] = True
			return redirect ('/sucess')
		else:
			for key,value in errors.items():
				messages.error(request, value)
			form = (request.POST)
			return redirect('/', {'form': form})
def login(request):
	if request.method == "POST":
		errors = User.objects.val_user(request.POST)
		if len(errors) < 1:
			email = request.POST['email']
			user = User.objects.get(email = email)
			request.session['first_name'] = user.first_name
			request.session['id'] = user.id
			request.session['logged_in'] = True
			return redirect ('/sucess')
		else:
			for key,value in errors.items():
				messages.error(request, value)
			form = (request.POST)
			return redirect('/', {'form': form})
def success(request):
	if 'logged_in' not in request.session:
		return redirect('/')
	context ={
		'show_job':Job.objects.all()
	}
	return render(request, 'default/success.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')
def process(request):
	if 'logged_in' not in request.session:
		return redirect('/')
	if request.method == 'POST':
		errors = Job.objects.isValid(request.POST)
	if len(errors) < 1:
		Job.objects.create(job = request.POST['job'], desc = request.POST['desc'], location = request.POST['location'], uploader = User.objects.get(id=request.session['id']))
	else:
		for key,value in errors.items():
			messages.error(request, value)
		form = (request.POST)
		return redirect('/addjob', {'form': form})
	return redirect('/sucess')

def addjob(request):
	if 'logged_in' not in request.session:
		return redirect('/')
	return render(request, "default/addjob.html")
def viewjob(request, id):
	if 'logged_in' not in request.session:
		return redirect('/')
	J = Job.objects.get(id = id)
	print(J.job)
	context ={
		"J" : J

	}
	return render(request, "default/viewjob.html",context)
def delete(request):
	if 'logged_in' not in request.session:
		return redirect('/')
	j = Job.objects.get(id=request.POST["displayJobid"])
	j.delete()
	return redirect("/sucess")
def edit(request, id):
	if 'logged_in' not in request.session:
		return redirect('/')
	J = Job.objects.get(id = id)
	print(J.job)
	context = {
	'J': J }
	return render(request, 'default/edit.html', context)
def editprocess(request):
	if request.method == "POST":
		J = Job.objects.get(id = request.POST["Jobid"] )
		J.job = request.POST['job']
		J.desc = request.POST['desc']
		J.location = request.POST['loaction']
		J.save()
		return redirect('/sucess')






# def show(request):
# 	context= {
# 	use = Users.objects.all()
# }
# return render(request, )


