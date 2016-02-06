from __future__ import unicode_literals

from hashid.models import HashID
from django.db import models

# Create your models here.

class Redirection(models.Model):
    hashid = models.OneToOneField(HashID, on_delete=models.PROTECT,
                                  related_name='hpshorten_redirect')
    url = models.CharField(max_length=4096)
    permanent = models.BooleanField(default=False)  # Use HTTP 301


class StaticRedirection(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    redirection = models.ForeignKey(Redirection, on_delete=models.PROTECT)
