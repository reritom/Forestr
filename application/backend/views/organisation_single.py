from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.organisation import Organisation
from backend.models.profile import Profile
from backend.models.survey import Survey
from backend.serialisers.survey_serialiser import SurveySerialiser
from backend.serialisers.profile_serialiser import ProfileSerialiser
from backend.serialisers.organisation_serialiser import OrganisationSerialiser
from backend.tools.decorators import Attach, login_required, attach_profile
from backend.tools.model_tools import get_surveys_of_organisation, get_profiles_of_organisation

from backend.tools.response_tools import (
    created,
    ok,
    accepted,
    not_permitted
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
class SingleOrganisationView(View):
    @method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'))
    def get(self, request, profile, organisation, resource=None):
        if not organisation == profile.organisation:
            return not_permitted("Attempting to access organisation you dont belong to")

        serialised = {
            'organisation': OrganisationSerialiser.serialise(organisation),
            'surveys': [
                SurveySerialiser.serialise(survey)
                for survey
                in get_surveys_of_organisation(organisation)
            ]
        }

        # If moderator, get users
        if profile.is_moderator:
            serialised['users'] = [
                ProfileSerialiser.serialise(profile)
                for profile in
                get_profiles_of_organisation
            ]

        return ok(serialised)

    @method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'))
    def patch(self, request, profile, organisation, resource=None):
        if not organisation == profile.organisation:
            return not_permitted("Attempting to access organisation you dont belong to")

        # TODO Assign moderator
        if profile.is_moderator:
            pass

        # Remove moderator (if owner)
        if profile.is_owner_of(organisation):
            pass

        # Change owner (if owner)
        if profile.is_owner_of(organisation):
            pass

        # Add user
        if profile.is_moderator:
            pass

        serialised = {
            'organisation': OrganisationSerialiser.serialise(organisation)
        }

        # If moderator, get users
        if profile.is_moderator:
            profiles = Profile.objects.filter(organisation=organisation)
            serialised['users'] = [ProfileSerialiser.serialise(profile) for profile in profiles]

        return accepted(serialised)

    @method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'))
    def delete(self, request, profile, organisation):
        return accepted({
            'message': f"organisation {organisation.id} has been deleted"
        })
