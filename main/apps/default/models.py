from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
from bcrypt import checkpw
import re

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class JobManager(models.Manager):
	def isValid(self, jobInfo):
		errors={}
		if len(jobInfo['job']) < 4:
			errors['job'] = "job title has to be 3 characters"
		if len(jobInfo['desc']) < 11:
			errors['decription'] = "description needs to be 11 characters"
		if len(jobInfo['location']) < 1:
			errors['location'] = "Location can't be blank"
		return errors
class UserManager(models.Manager):
	def isValidRegistration(self, userInfo):
		errors={}
		if not userInfo['first_name'].isalpha():
		    errors['first_name'] = "Enter a valid first name with no numbers"
		if not userInfo['last_name'].isalpha():
		    errors['last_name'] = "last name can't have numbers"
		if not EMAIL_REGEX.match(userInfo['email']):
		    errors['email'] = "Enter a valid email address"
		if len(userInfo['password']) < 7:
		    errors['password'] = "password has to be at least 8 char"
		if User.objects.filter(email = userInfo['email']):
			errors['email'] = "This email already emails"
		else:
			errors['sucess'] =  "Success! Welcome, " + userInfo['first_name'] + "!"
			hashed = bcrypt.hashpw(userInfo['password'].encode(), bcrypt.gensalt())
			User.objects.create(first_name = userInfo['first_name'], last_name = userInfo['last_name'], email = userInfo['email'], password = hashed)
		return errors
	
	def val_user(self, userInfo):
		email = userInfo['email']
		U = User.objects.filter(email = email).first()
		errors = {}
		if not EMAIL_REGEX.match(userInfo['email']):
		    errors['email'] = "Enter a valid email address"
		if len(userInfo['email']) < 7:
		    errors['email'] = "Enter in a valid email"
		if bcrypt.checkpw(userInfo['password'].encode(), U.password.encode()):
			print (U.first_name)
		else:
			errors['pass'] = "This password is incorrect"
		return errors
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class Job(models.Model):
	job = models.CharField(max_length=1000)
	desc = models.CharField(max_length=1000)
	location = models.CharField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	uploader = models.ForeignKey(User, related_name="uploaded_jobs", null=True, default=None, on_delete=models.CASCADE,)
	objects = JobManager()
