from django.db import models
from django.utils import timezone
from backend.models.organisation import Organisation
from django.contrib.auth.models import User

import uuid

class Contract(models.Model):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"

    INVITE = "invite"
    REQUEST = "request"
    OWNERSHIP_TRANSFER = "ownership_transfer"

    id = models.CharField(max_length=255, unique=True, primary_key=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255, default=PENDING)
    contract_type = models.CharField(max_length=255)

    @classmethod
    def make(cls, *args, **kwargs):
        def generate_uuid():
            id = str(uuid.uuid4())
            if cls.objects.filter(id=id).exists():
                return generate_uuid()
            return id

        kwargs.setdefault('id', generate_uuid())
        return cls.objects.create(*args, **kwargs)
