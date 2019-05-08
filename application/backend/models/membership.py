from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from backend.models.organisation import Organisation

from datetime import datetime, timedelta
import uuid

class Membership(models.Model):
    ORIGIN_OWNER = "owner"
    ORIGIN_INVITE = "invite"
    ORIGIN_REQUEST = "request"

    id = models.CharField(max_length=255, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    moderator = models.BooleanField(default=False)
    joined = models.DateTimeField(default=timezone.now)
    origin = models.CharField(max_length=255) # INVITE or REQUEST or OWNER

    @classmethod
    def make(cls, *args, **kwargs):
        def generate_uuid():
            id = str(uuid.uuid4())
            if cls.objects.filter(id=id).exists():
                return generate_uuid()
            return id

        kwargs.setdefault('id', generate_uuid())
        return cls.objects.create(*args, **kwargs)

    @property
    def is_owner(self):
        return self.organisation.owner == self.user

    def set_moderator(self, value=True):
        self.moderator = value
        self.save()

    def unset_moderator(self):
        self.moderator = False
        self.save()
