from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.organisation import Organisation
from backend.serialisers.organisation_serialiser import OrganisationSerialiser
from backend.tools.decorators import Attach, attach_profile, login_required

from backend.tools.response_tools import (
    conflict,
    created
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
class OrganisationView(View):
    def post(self, request, profile):
        if profile.organisation.enterprise:
            return conflict("User already part of an organisation")

        if Organisation.objects.filter(name=request.POST['name']).exists():
            return conflict(f"Organisation name {request.POST['name']} taken")

        if Organisation.objects.filter(owner=profile.user, enterprise=True).exists():
            return conflict("User already owner of organisation")

        organisation = Organisation.make(
            name=request.POST['name'],
            description=request.POST['description'],
            owner=request.user,
            enterprise=True,
            personal=False
        )

        profile.set_organisation(organisation, moderator=True)

        return created({
            'organisation': OrganisationSerialiser.serialise(organisation)
        })
