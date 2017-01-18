# coding: utf-8

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Meeting
from organizer.tools import ErrorMessage, IsNullOrEmpty, HtmlDateParse

@login_required
def index(request):
    meetings = Meeting.objects.filter(user=request.user)
    context = { 'meetings': meetings }
    return render(request, 'meetings/index.html', context)

@login_required
def add(request):
    return render(request, 'meetings/add.html')

@login_required
def addsubmit(request):
    error = ErrorMessage()

    title = request.POST.get("title")
    description = request.POST.get("description")
    begin = request.POST.get("begin")
    end = request.POST.get("end")
    send_email = request.POST.get("send_email") == "on"
    email_date = request.POST.get("email_date")

    #print("begin: '{}', end: '{}'".format(begin, end))

    if IsNullOrEmpty(title):
        error.set("Musisz podać tytuł spotkania!")
    elif IsNullOrEmpty(begin) or IsNullOrEmpty(end):
        error.set("Musisz podać datę spotkania!")
    elif send_email and IsNullOrEmpty(email_date):
        error.set("Musisz podać datę emaila!")

    if error.good() and description is not None:
        description = description.strip()

    if error.good():
        date_from = HtmlDateParse(begin)
        date_to = HtmlDateParse(end)
        if date_from is None or date_to is None:
            error.set("Data spotkania jest nieprawidłowa!")
        elif date_from <= timezone.now():
            error.set("Data spotkania musi wyprzedzać aktualny czas!")
        elif date_to < date_from:
            error.set("Przedział czasowy spotkania jest nieprawidłowy!")

    if error.good() and send_email:
        email_date = HtmlDateParse(email_date)
        if email_date is None:
            error.set("Data emaila jest nieprawidłowa!")
        elif email_date <= timezone.now():
            error.set("Data emaila musi wyprzedzać aktualny czas!")
        elif email_date > date_from:
            error.set("Data emaila musi poprzedzać datę spotkania!")

    context = {'error': str(error)}

    if error.good():
        meeting = Meeting()
        meeting.user = request.user
        meeting.title = title
        meeting.description = (description if len(description) > 0 else None)
        meeting.begin = date_from
        meeting.end = date_to
        meeting.send_email = send_email
        meeting.email_date = (email_date if send_email else None)
        meeting.email_was_send = False
        meeting.save()

        context.update({'meeting': meeting})

    return render(request, 'meetings/addsubmit.html', context)

@login_required
def show(request, meeting_id):
    error = ErrorMessage()

    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except:
        error.set("Spotkanie o podanym ID nie istnieje!")
    else:
        if meeting.user != request.user:
            error.set("Nie jesteś właścicielem tego spotkania!")

    context = {'error': str(error)}

    if error.good():
        context.update({'meeting': meeting})

    return render(request, 'meetings/show.html', context)

@login_required
def remove(request, meeting_id):
    error = ErrorMessage()

    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except:
        error.set("Spotkanie o podanym ID nie istnieje!")
    else:
        if meeting.user != request.user:
            error.set("Nie jesteś właścicielem tego spotkania!")

    if error.good():
        meeting.delete()

    context = {'error': str(error)}

    return render(request, 'meetings/remove.html', context)
