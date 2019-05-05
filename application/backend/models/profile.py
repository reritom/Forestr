from django.db import models
from django.contrib.auth.models import User
from backend.models.organisation import Organisation

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, null=True)
    moderator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def is_owner_of(self, organisation):
        return self.user == organisation.owner

    def is_moderator(self):
        return self.moderator

    def set_organisation(self, organisation, moderator=False):
        self.organisation = organisation
        self.moderator = moderator
        self.save()
