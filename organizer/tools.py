# -*- coding: utf-8 -*-

import sys
import logging

from threading import Timer
from django.utils import timezone
from datetime import datetime

# Globals

_checkEmailsTimer = None

# Functions

def ValidateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        
    def start(self, runOnInit=False):
        if not self.isRunning():
            if runOnInit:
                self._run_function()
            self._create_timer()
            
    def stop(self):
        if self.isRunning():
            self._delete_timer()
            
    def isRunning(self):
        return self._timer is not None
    
    def _run(self):
        self.stop()
        self._run_function()
        self.start(False)
        
    def _run_function(self):
        self.function(*self.args, **self.kwargs)
        
    def _create_timer(self):
        self._timer = Timer(self.interval, self._run)
        self._timer.start()
        
    def _delete_timer(self):
        self._timer.cancel()
        self._timer = None

def CropStr(text, n):
    if len(text) > n:
        return text[:n] + '...'
    
    return text

class ErrorMessage(object):
    def __init__(self):
        self._error = False
        self.message = ""
        
    def get(self):
        return self.message
    
    def set(self, msg):
        self._error = True
        self.message = msg
        
    def good(self):
        return not self._error
    
    def __str__(self):
        return self.get()

def GetPost(request, values):
    result = {}
    
    for key in values:
        post_value = request.POST.get(key, '')
        
        if len(post_value.strip()) == 0:
            result[key] = ''
        else:
            result[key] = post_value
            
    return result

def IsNullOrEmpty(text):
    if text is None:
        return True
    if not isinstance(text, str) and not isinstance(text, unicode):
        return True
    if len(text.strip()) == 0:
        return True
    return False

def OneIsNullOrEmpty(*args):
    for arg in args:
        if IsNullOrEmpty(arg):
            return True
    return False

def IsLinux():
    return sys.platform == 'linux' or sys.platform == 'linux2'

def HtmlDateParse(dateString, dateFormat = '%d.%m.%Y %H:%M'):
    try:
        date_naive = datetime.strptime(dateString, dateFormat)
        date_aware = timezone.make_aware(date_naive)
    except:
        return None
    else:
        return date_aware

def CheckOrganizerApps():
    from django.conf import settings
    if settings.CHECK_EMAILS_ENABLED:
        
        OrganizerLogDebug("Checking apps for sending emails...")
        
        from jobs.apps import JobsCheckEmails
        JobsCheckEmails()
        
        from meetings.apps import MeetingsCheckEmails
        MeetingsCheckEmails()
        
        OrganizerLogDebug("Apps checked for emails.")

def InitAppsCheckingSystem():
    global _checkEmailsTimer
    
    if _checkEmailsTimer is None:
        from django.conf import settings
        
        OrganizerLogDebug("Creating checkEmailsTimer...")
        
        _checkEmailsTimer = RepeatedTimer(settings.CHECK_EMAILS_DELAY, CheckOrganizerApps)
        
        OrganizerLogDebug("checkEmailsTimer created.")
        
        _checkEmailsTimer.start(False)
        
        OrganizerLogInfo("checkEmailsTimer started.")
    else:
        OrganizerLogInfo("checkEmailsTimer already exists.")
        
def OrganizerLogDebug(msg):
    logging.getLogger("organizer").debug(msg)
def OrganizerLogInfo(msg):
    logging.getLogger("organizer").info(msg)
def OrganizerLogWarning(msg):
    logging.getLogger("organizer").warning(msg)
def OrganizerLogError(msg):
    logging.getLogger("organizer").error(msg)
def OrganizerLogFatal(msg):
    logging.getLogger("organizer").fatal(msg)
    
