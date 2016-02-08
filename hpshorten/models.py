from __future__ import unicode_literals

from hashid.models import HashID
from django.db import models

# Create your models here.

class Redirection(models.Model):
    hashid = models.OneToOneField(HashID, on_delete=models.PROTECT,
                                  related_name='hpshorten_redirect')
    url = models.CharField(max_length=4096)
    permanent = models.BooleanField(default=False)  # Use HTTP 301

    cloak = models.BooleanField(default=False)  # use iframe (conflicts with permanent)
    title = models.CharField(max_length=255, default="")  # only used when cload == True

    def __unicode__(self):
        ret = '[{}]({})'.format(self.hashid.hashid, self.url)
        if self.permanent:
            ret += ' [301]'
        if self.cloak:
            ret += ' [FRAME]'
        return ret


class StaticRedirection(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    redirection = models.ForeignKey(Redirection, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.id
