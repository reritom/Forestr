from django.db import models
from django.contrib.auth.models import User
from backend.models.organisation import Organisation

import uuid

class Setting(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    user = models.ForeignKey(User, null=True)
    organisation = models.ForeignKey(Organisation, null=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    @classmethod
    def make(cls, *args, **kwargs):
        def generate_uuid():
            id = str(uuid.uuid4())
            if cls.objects.filter(id=id).exists():
                return generate_uuid()
            return id

        kwargs.setdefault('id', generate_uuid())
        return cls.objects.create(*args, **kwargs)
