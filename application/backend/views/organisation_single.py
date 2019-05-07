from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.organisation import Organisation
from backend.models.profile import Profile

from backend.serialisers.profile_serialiser import ProfileSerialiser
from backend.serialisers.organisation_serialiser import OrganisationSerialiser

from backend.tools.decorators import Attach, Assert, login_required, attach_profile
from backend.tools.form import Form
from backend.tools.model_tools import (
    get_surveys_of_organisation,
    get_profiles_of_organisation,
    get_items_of_organisation
)
from backend.tools.response_tools import (
    created,
    ok,
    accepted,
    not_permitted
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
@method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'), name="dispatch")
@method_decorator(Assert.that('profile.organisation').equals('organisation'), name="dispatch")
class SingleOrganisationView(View):
    def get(self, request, profile, organisation):
        serialised = {
            'organisation': OrganisationSerialiser.serialise(organisation)
        }

        # If moderator, get users
        if profile.is_moderator:
            serialised['users'] = [
                ProfileSerialiser.serialise(profile)
                for profile in
                get_profiles_of_organisation(organisation)
            ]

        return ok(serialised)

    def patch(self, request, profile, organisation):
        if not profile.is_moderator:
            return not_permitted("Only moderators or owners can update the organisation")

        form = {}

        # Change the name
        if form.name:
            if profile.is_owner_of(organisation):
                organisation.change_name(form.name)
            else:
                return not_permitted("Only the owner can change the organisation name")

        # Change owner
        if form.owner:
            if profile.is_owner_of(organisation):
                # Get the account for that user
                # Check they are a member of this organisation
                # Create the contract
                pass

        # Add user
        if form.new_members:
            if profile.is_moderator:
                pass

        # Remove user
        if form.remove_members:
            if profile.is_moderator:
                pass

        # Add moderator
        if form.add_moderator:
            if profile.is_moderator:
                # Get the profile, check it is already a member
                pass

        # Remove moderator
        if form.remove_moderator:
            if profile.is_moderator:
                pass

        serialised = {
            'organisation': OrganisationSerialiser.serialise(organisation)
        }

        # If moderator, get users
        if profile.is_moderator:
            profiles = Profile.objects.filter(organisation=organisation)
            serialised['users'] = [
                ProfileSerialiser.serialise(profile)
                for profile in
                get_profiles_of_organisation(organisation)
            ]

        return accepted(serialised)

    def delete(self, request, profile, organisation):
        #TODO Only owners of enterprise organisations can delete the organisation (requires email confirmation)
        # On confirmation, all profiles are returned to their personal organisation
        return accepted({'message': f"organisation {organisation.id} has been deleted"})
