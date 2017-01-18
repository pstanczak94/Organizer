# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.template.loader import render_to_string
from organizer.tools import CropStr,\
    OrganizerLogDebug, OrganizerLogInfo, OrganizerLogError

class MeetingsConfig(AppConfig):
    name = 'meetings'
    verbose_name = 'Meetings'
    
    def ready(self):
        AppConfig.ready(self)

def MeetingsCheckEmails():
    from django.utils import timezone
    from meetings.models import Meeting
    
    OrganizerLogDebug("Checking meetings to send emails...")
    
    date_now = timezone.now()
    meetings_list = Meeting.objects.all()
    
    for meeting in meetings_list:
        if not meeting.send_email or meeting.email_was_send:
            continue
        if meeting.email_date >= date_now:
            continue
        if date_now > meeting.begin:
            continue

        MeetingsSendEmail(meeting)

def MeetingsSendEmail(meeting):
    OrganizerLogDebug("<meetings> Sending email to: %s, ID: %d, Title: %s" % 
          (meeting.user.email, meeting.id, CropStr(meeting.title, 20)))
    
    subject = "[Organizer] Spotkanie - " + str(meeting)
    
    context = { 'meeting': meeting }
    
    text_content = render_to_string('meetings/mail.txt', context)
    html_content = render_to_string('meetings/mail.html', context)

    try:
        meeting.user.email_user(subject, text_content, html_message=html_content)
    except:
        OrganizerLogError("<meetings> Cannot send email to %s!" % (meeting.user.email))
    else:
        OrganizerLogInfo("<meetings> Email send to %s." % (meeting.user.email))
        meeting.email_was_send = True
        meeting.save()

