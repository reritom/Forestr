from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.organisation import Organisation
from backend.models.profile import Profile
from backend.serialisers.profile_serialiser import ProfileSerialiser
from backend.serialisers.organisation_serialiser import OrganisationSerialiser
from backend.tools.decorators import Attach, login_required, attach_profile

from backend.tools.response_tools import (
    created,
    ok,
    accepted
)

@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
class SingleOrganisationView(View):
    @method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'))
    def get(self, request, profile, organisation):
        serialised = {
            'organisation': OrganisationSerialiser.serialise(organisation)
        }

        # If moderator, get users
        if profile.is_moderator:
            profiles = Profile.objects.filter(organisation=organisation)
            serialised['users'] = [ProfileSerialiser.serialise(profile) for profile in profiles]

        items = "Hi"
        # If any, get all surveys
        return ok(serialised)

    @method_decorator(csrf_exempt)
    @method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'))
    def patch(self, request, profile, organisation, resource=None):
        # TODO Assign moderator
        if profile.is_moderator_of(organisation):
            pass

        # Remove moderator (if owner)

        # Change owner (if owner)
        if profile.is_owner_of(organisation):
            pass

        # Add user

        return accepted({
            'organisation': OrganisationSerialiser.serialise(organisation)
        })

    @method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'))
    def delete(self, request, profile, organisation):
        return accepted({
            'message': f"organisation {organisation.id} has been deleted"
        })
