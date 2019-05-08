from django.db import models
from django.utils import timezone
from backend.models.profile import Profile
from backend.models.organisation import Organisation

import uuid

class Event(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, null=True)
    created = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255)

    @classmethod
    def make(cls, *args, **kwargs):
        def generate_uuid():
            id = str(uuid.uuid4())
            if cls.objects.filter(id=id).exists():
                return generate_uuid()
            return id

        kwargs.setdefault('id', generate_uuid())
        return cls.objects.create(*args, **kwargs)
