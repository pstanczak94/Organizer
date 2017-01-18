#coding: utf-8

from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

from .models import Job
from organizer.tools import ErrorMessage

@login_required
def index(request):
	job_list = Job.objects.filter(user=request.user)
	context = { 'job_list': job_list }
	return render(request, 'jobs/index.html', context)

@login_required
def add(request):
	date_now = timezone.now()
	prefjobdate = date_now + timedelta(days=1)
	prefemaildate = prefjobdate - timedelta(hours=1)
	context = {
		'date_now': date_now,
		'prefjobdate': prefjobdate,
		'prefemaildate': prefemaildate
	}
	return render(request, 'jobs/add.html', context)

@login_required
def addsubmit(request):
	error = ErrorMessage()
	job = Job()
	
	date_now = timezone.now()

	post_title = request.POST.get("title", "")
	post_description = request.POST.get("description", "")
	post_date = request.POST.get("date", "")
	post_sendemail = request.POST.get("sendemail", "")
	post_emaildate = request.POST.get("emaildate", "")
	
	fixed_date = date_now
	fixed_email_date = date_now
	fixed_sendemail = (post_sendemail != "")
	
	if post_title == "":
		error.set("Musisz podać tytuł zadania!")
	#elif post_description == "":
	#	error.set("Musisz podać treść zadania!")
	elif post_date == "":
		error.set("Musisz podać datę zadania!")
	elif fixed_sendemail and post_emaildate == "":
		error.set("Musisz podać datę emaila!")

	if error.good():
		try:
			fixed_date = datetime.strptime(post_date, "%Y-%m-%dT%H:%M")
			fixed_date = timezone.make_aware(fixed_date)
		except:
			error.set("Data zadania jest nieprawidłowa!")
		else:
			if fixed_date <= date_now:
				error.set("Data zadania musi wyprzedzać aktualny czas!")
	
	if fixed_sendemail and error.good():
		try:
			fixed_email_date = datetime.strptime(post_emaildate, "%Y-%m-%dT%H:%M")
			fixed_email_date = timezone.make_aware(fixed_email_date)
		except:
			error.set("Data emaila jest nieprawidłowa!")
		else:
			if fixed_email_date <= date_now:
				error.set("Data emaila musi wyprzedzać aktualny czas!")
			elif fixed_email_date > fixed_date:
				error.set("Data emaila musi poprzedzać datę zadania!")
	
	if error.good():
		job.user = request.user
		job.title = post_title
		job.description = post_description
		job.date = fixed_date
		job.send_email = fixed_sendemail
		job.email_date = fixed_email_date
		job.email_was_send = False
		job.save()
		
	context = {
		'date_now': date_now,
		'no_error': error.good(),
		'error_message': error.message
	}
	
	if error.good():
		context.update({
			'id': job.id,
			'jobdate': job.date,
			'title': job.title,
			'description': job.description,
			'sendemail': job.send_email,
			'emailwassend': job.email_was_send,
			'emaildate': job.email_date
		})
	
	return render(request, 'jobs/addsubmit.html', context)

@login_required
def show(request, job_id):
	error = ErrorMessage()
	
	try:
		job = Job.objects.get(id=job_id)
	except:
		error.set("Zadanie o podanym ID nie istnieje!")
	else:
		if job.user != request.user:
			error.set("Nie jesteś właścicielem tego zadania!")
	
	context = {
		'no_error': error.good(),
		'error_message': error.message
	}
	
	if error.good():
		context.update({
			'id': job.id,
			'jobdate': job.date,
			'title': job.title,
			'description': job.description,
			'sendemail': job.send_email,
			'emailwassend': job.email_was_send,
			'emaildate': job.email_date
		})
	
	return render(request, 'jobs/show.html', context)

@login_required
def remove(request, job_id):
	error = ErrorMessage()
	
	try:
		job = Job.objects.get(id=job_id)
	except:
		error.set("Zadanie o podanym ID nie istnieje!")
	else:
		if job.user != request.user:
			error.set("Nie jesteś właścicielem tego zadania!")
	
	if error.good():
		job.delete()
	
	context = {
		'no_error': error.good(),
		'error_message': error.message
	}
	
	return render(request, 'jobs/remove.html', context)
