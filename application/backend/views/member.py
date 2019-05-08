from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.contract import Contract
from backend.models.membership import Membership
from backend.serialisers.contract_serialiser import ContractSerialiser
from backend.serialisers.membership_serialiser import MembershipSerialiser
from backend.tools.decorators import Attach, attach_profile, login_required
from backend.tools.form import Form

from backend.tools.model_tools import (
    get_members_of_organisation
)

from backend.tools.response_tools import (
    conflict,
    created,
    not_permitted,
    ok
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
class MemberView(View):
    def post(self, request, profile):
        """
        To add a member to an organisation, we create a contract which needs confirming by the other party before
        the membership is applied.
        """
        membership = Membership.objects.get(user=profile.user)

        if not membership.organisation.enterprise:
            return not_permitted("Personal organisation can't have additional members")

        if membership.moderator:
            contract = Contract.make(
                contract_type=Contract.INVITE,
                organisation=membership.organisation,
                user=membership.user
            )
        else:
            return not_permitted("Only moderators can add members")

        return created({
            'message': "Request sent to user",
            'contract': ContractSerialiser.serialise(contract)
        })

    def get(self, request, profile):
        request_membership = Membership.objects.get(user=profile.user)

        if not request_membership.moderator:
            return not_permitted("Only moderators can view members")

        return ok({
            'members': [
                MembershipSerialiser.serialise(member)
                for member in
                get_members_of_organisation(request_membership.organisation)
            ]
        })
