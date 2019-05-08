from django.db import models
from django.utils import timezone
from django.conf import settings
from backend.models.organisation import Organisation

from datetime import datetime, timedelta
import uuid

class Item(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    external_id = models.CharField(max_length=255)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255, null=True)
    photos = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(default=timezone.now, null=True)
    location = models.CharField(max_length=255, null=True)
    location_description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.id} {self.created}"

    def set_external_id(self, id):
        self.external_id = id
        self.save()

    @classmethod
    def make(cls, *args, **kwargs):
        def generate_uuid():
            id = str(uuid.uuid4())
            if cls.objects.filter(id=id).exists():
                return generate_uuid()
            return id

        kwargs.setdefault('id', generate_uuid())
        return cls.objects.create(*args, **kwargs)
