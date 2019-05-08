from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.organisation import Organisation
from backend.models.profile import Profile
from backend.models.membership import Membership

from backend.serialisers.profile_serialiser import ProfileSerialiser
from backend.serialisers.organisation_serialiser import OrganisationSerialiser

from backend.tools.decorators import Attach, Assert, login_required, attach_profile
from backend.tools.form import Form
from backend.tools.model_tools import (
    get_surveys_of_organisation,
    get_profiles_of_organisation,
    get_items_of_organisation
)
from backend.tools.response_tools import ok

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
@method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'), name="dispatch")
class SingleOrganisationView(View):
    def get(self, request, profile, organisation):
        return ok({'organisation': OrganisationSerialiser.serialise(organisation)})
