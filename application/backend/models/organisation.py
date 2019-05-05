from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from datetime import datetime, timedelta
import uuid

class Organisation(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(default=timezone.now, null=True)
    description = models.CharField(max_length=255)
    personal = models.BooleanField(default=True)
    enterprise = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def make(cls, *args, **kwargs):
        def generate_uuid():
            id = str(uuid.uuid4())
            print(f"Generating uuid {id}")
            if cls.objects.filter(id=id).exists():
                return generate_uuid()
            return id

        kwargs.setdefault('id', generate_uuid())
        return cls.objects.create(*args, **kwargs)
