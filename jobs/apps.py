# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.template.loader import render_to_string
from organizer.tools import CropStr,\
    OrganizerLogDebug, OrganizerLogInfo, OrganizerLogError

class JobsConfig(AppConfig):
    name = 'jobs'
    verbose_name = 'Jobs'
    
    def ready(self):
        AppConfig.ready(self)

def JobsCheckEmails():
    from django.utils import timezone
    from jobs.models import Job
    
    OrganizerLogDebug("Checking jobs to send emails...")
    
    date_now = timezone.now()
    job_list = Job.objects.all()
    
    for job in job_list:
        if not job.send_email or job.email_was_send:
            continue
        if job.email_date >= date_now:
            continue
        if date_now > job.date:
            continue

        JobsSendEmail(job)

def JobsSendEmail(job):
    OrganizerLogDebug("<jobs> Sending email to: %s, ID: %d, Title: %s" % 
          (job.user.email, job.id, CropStr(job.title, 20)))
    
    subject = "[Organizer] Zadanie - " + str(job)
    
    context = { 'job': job }
    
    text_content = render_to_string('jobs/mail.txt', context)
    html_content = render_to_string('jobs/mail.html', context)

    try:
        job.user.email_user(subject, text_content, html_message=html_content)
    except:
        OrganizerLogError("<jobs> Cannot send email to %s!" % (job.user.email))
    else:
        OrganizerLogInfo("<jobs> Email send to %s." % (job.user.email))
        job.email_was_send = True
        job.save()
