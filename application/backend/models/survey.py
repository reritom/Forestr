from django.db import models
from django.utils import timezone
from django.conf import settings

from backend.models.organisation import Organisation

from datetime import datetime, timedelta
import uuid

class Survey(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    description = models.CharField(max_length=255)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    survey_type = models.CharField(max_length=255, default="Misc")
    status = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.id} {self.created}"

    @classmethod
    def make(cls, *args, **kwargs):
        def generate_uuid():
            id = str(uuid.uuid4())
            if cls.objects.filter(id=id).exists():
                return generate_uuid()
            return id

        kwargs.setdefault('id', generate_uuid())
        return cls.objects.create(*args, **kwargs)
