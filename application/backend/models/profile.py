from django.db import models
from django.contrib.auth.models import User
from backend.models.organisation import Organisation

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, null=True)

    def __str__(self):
        return self.user.username
