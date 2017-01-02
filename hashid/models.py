from __future__ import unicode_literals

import config
from hpurl.settings import SECRET_KEY
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

import hashids

# Create your models here.

public_hash = hashids.Hashids(SECRET_KEY, config.KEY_LENGTH_PUBLIC)
private_hash = hashids.Hashids(SECRET_KEY, config.KEY_LENGTH_PRIVATE)

class HashID(models.Model):
    id = models.AutoField(primary_key=True)
    private = models.BooleanField(default=False)

    enabled = models.BooleanField(default=True)

    create_time = models.DateTimeField(auto_now_add=True)
    last_access_time = models.DateTimeField(auto_now=True)

    view_count = models.IntegerField(default=0)

    def __unicode__(self):
        ret = '{} ({} Hits)'.format(self.hashid, self.view_count)
        if not self.enabled:
            ret += ' [DISABLED]'
        return ret

    @property
    def hashid(self):
        return private_hash.encode(self.id) if self.private \
                else public_hash.encode(self.id)

    @classmethod
    def get(cls, hashid, inc=True):
        if len(hashid) >= config.KEY_LENGTH_PRIVATE:
            uid = private_hash.decode(hashid)
        else:
            uid = public_hash.decode(hashid)
        try:
            uid = uid[0]
        except IndexError:
            raise Http404("Hashid {} not found".format(hashid))
        model = get_object_or_404(cls, id=uid, enabled=True)
        if inc:
            model.view_count = models.F("view_count") + 1
            model.save()
        return model

    @classmethod
    def get_related(cls, hashid, key, inc=True):
        model = cls.get(hashid, inc)
        try:
            ret = getattr(model, key)
        except ObjectDoesNotExist:
            raise Http404("Hashid {} not found".format(hashid))
        return ret

    @classmethod
    def new(cls, private):
        model = cls(private=private)
        model.save()
        return model
