from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.organisation import Organisation
from backend.serialisers.organisation_serialiser import OrganisationSerialiser

from backend.tools.response_tools import (
    conflict,
    created
)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class OrganisationView(View):
    def post(self, request):
        try:
            organisation = Organisation.make(
                name=request.POST['name'],
                description=request.POST['description'],
                owner=request.user
            )
        except Exception as e:
            return conflict(f"Organisation name taken")

        return created({
            'organisation': OrganisationSerialiser.serialise(organisation)
        })
