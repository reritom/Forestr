from django.db import models
from django.utils import timezone
from django.conf import settings

from datetime import datetime, timedelta
import uuid

class Example(models.Model):
    unique_string = models.CharField(default=0, max_length=255, unique=True)
    created = models.DateTimeField(default=timezone.now, null=True)
    boolean = models.BooleanField(default=False)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.unique_string

    def set_boolean(self, value: bool):
        self.boolean = bool
        self.save()
