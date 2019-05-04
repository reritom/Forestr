from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.organisation import Organisation
from backend.serialisers.organisation_serialiser import OrganisationSerialiser
from backend.tools.decorators import Attach

from backend.tools.response_tools import (
    created,
    ok,
    accepted
)

@method_decorator(login_required, name="dispatch")
class SingleOrganisationView(View):
    @method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'))
    def get(self, request, organisation):
        return ok({
            'organisation': OrganisationSerialiser.serialise(organisation)
        })

    @method_decorator(csrf_exempt)
    @method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'))
    def patch(self, request, organisation):
        return accepted({
            'organisation': OrganisationSerialiser.serialise(organisation)
        })

    @method_decorator(Attach.incoming('organisation_id').to(Organisation).as_outgoing('organisation'))
    def delete(self, request, organisation):
        return accepted({
            'message': f"organisation {organisation.id} has been deleted"
        })
