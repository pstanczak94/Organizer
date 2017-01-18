# -*- coding: utf-8 -*-

import re

from django.shortcuts import render, redirect
from organizer.tools import IsNullOrEmpty, ValidateEmail, GetPost, OneIsNullOrEmpty
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from organizer import settings
from django.urls.base import reverse

_index_template = 'index.html'
_login_template = 'account/login.html'
_logged_in_template = 'account/logged_in.html'
_logout_template = 'account/logout.html'
_logged_out_template = 'account/logged_out.html'
_create_template = 'account/create.html'
_created_template = 'account/created.html'

def index(request):
	return render(request, _index_template)

def account_login(request):
	if request.method == 'GET':
		context = {'next':request.GET.get('next', '')}
		return render(request, _login_template, context)
	
	post_values = ('username', 'password', 'next')
	post = GetPost(request, post_values)
	
	context = {}
	context.update(post)

	if IsNullOrEmpty(post['username']):
		context.update({'error': "Musisz podać login!"})
		return render(request, _login_template, context)
	
	if IsNullOrEmpty(post['password']):
		context.update({'error': "Musisz podać hasło!"})
		return render(request, _login_template, context)
	
	try:
		user = User.objects.get(username__iexact=post['username'])
	except User.DoesNotExist:
		context.update({'error': "Nie istnieje użytkownik o podanym loginie!"})
		return render(request, _login_template, context)
	
	username = user.username
	
	user = authenticate(username=username, password=post['password'])
	
	if user is None:
		context.update({'error': "Podane hasło jest nieprawidłowe!"})
		return render(request, _login_template, context)
	
	login(request, user)
	
	next_page = post['next']
	
	if IsNullOrEmpty(next_page):
		next_page = settings.LOGIN_REDIRECT_URL
	
	return redirect(to=next_page)
	
def account_logged_in(request):
	return render(request, _logged_in_template)
	
def account_logout(request):
	logout(request)
	return redirect(to=settings.LOGOUT_REDIRECT_URL)

def account_logged_out(request):
	return render(request, _logged_out_template)

def account_create(request):
	if request.method == 'POST':
		post_values = ('username', 'password1', 'password2', 'email')
		post = GetPost(request, post_values)

		context = {}
		context.update(post)
		
		if OneIsNullOrEmpty(post['username'], post['password1'], post['password2'], post['email']):
			context.update({'error':'Musisz wypełnić wszystkie pola!'})
			return render(request, _create_template, context)
		
		if not re.match(r'^[A-Za-z0-9]{3,30}$', post['username']):
			context.update({'error':'Podana nazwa użytkownika jest nieprawidłowa!'})
			return render(request, _create_template, context)
		
		if post['password1'] != post['password2']:
			context.update({'error':'Hasła się nie zgadzają!'})
			return render(request, _create_template, context)
		
		if not re.match(r'^.{3,20}$', post['password1']):
			context.update({'error':'Hasło jest nieprawidłowej długości!'})
			return render(request, _create_template, context)
		
		if not ValidateEmail(post['email']):
			context.update({'error':'Podany email jest nieprawidłowy!'})
			return render(request, _create_template, context)
		
		userExists = True
		
		try:
			User.objects.get(username__iexact=post['username'])
		except User.DoesNotExist:
			userExists = False
		
		if userExists:
			context.update({'error':'Istnieje już użytkownik o podanej nazwie!'})
			return render(request, _create_template, context)
		
		emailExists = True
		
		try:
			User.objects.get(email__iexact=post['email'])
		except User.DoesNotExist:
			emailExists = False
		
		if emailExists:
			context.update({'error':'Podany adres email jest już przypisany do innego konta!'})
			return render(request, _create_template, context)
	
		try:
			user = User.objects.create_user(post['username'], post['email'], post['password1'])
			user.save()
		except:
			context.update({'error':'Nie udało się stworzyć użytkownika!'})
			return render(request, _create_template, context)
		
		user = authenticate(username=post['username'], password=post['password1'])
		login(request, user)
		
		return redirect(to=reverse('created'))
		
	return render(request, _create_template)

def account_created(request):
	return render(request, _created_template)

