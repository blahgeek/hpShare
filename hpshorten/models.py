from __future__ import unicode_literals

from hashid.models import HashID
from django.db import models

# Create your models here.

class Redirection(models.Model):
    hashid = models.OneToOneField(HashID, on_delete=models.PROTECT,
                                  related_name='hpshorten_redirect')
    url = models.CharField(max_length=4096)
    permanent = models.BooleanField(default=False)  # Use HTTP 301

    def __unicode__(self):
        return '[{}]({})'.format(self.hashid.hashid, self.url)


class StaticRedirection(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    redirection = models.ForeignKey(Redirection, on_delete=models.PROTECT)
