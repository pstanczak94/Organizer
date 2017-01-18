from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format

@python_2_unicode_compatible
class Meeting(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    added = models.DateTimeField(default=timezone.now)
    send_email = models.BooleanField(default=False)
    email_date = models.DateTimeField(blank=True, null=True)
    email_was_send = models.BooleanField(default=False, blank=True)

    def __str__(self):
        fixed_date = timezone.make_naive(self.begin)
        datestr = DateFormat(fixed_date).format(get_format('DATE_FORMAT'))
        return "%s [%s]" % (self.title, datestr)