from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.membership import Membership
from backend.serialisers.membership_serialiser import MembershipSerialiser
from backend.tools.decorators import Attach, attach_profile, login_required
from backend.tools.form import Form

from backend.tools.response_tools import (
    accepted,
    ok,
    not_permitted
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
@method_decorator(Attach.incoming('member_id').to(Membership).as_outgoing('membership'), name="dispatch")
class SingleMemberView(View):
    def patch(self, request, profile, membership):
        """
        To add a member to an organisation, we create a contract which needs confirming by the other party before
        the membership is applied.
        """
        request_membership = Membership.objects.get(user=profile.user)
        form = Form.for_model(Membership).with_request(request)

        if not request_membership.moderator:
            return not_permitted("Only moderators can change members")

        if form.moderator is not None:
            membership.set_moderator(form.moderator)

        return accepted({'member': MembershipSerialiser.serialise(membership)})

    def delete(self, request, profile, membership):
        request_membership = Membership.objects.get(user=profile.user)

        if not request_membership.moderator:
            return not_permitted("Only moderators can delete members")

        if membership.moderator:
            if not request_membership.is_owner:
                return not_permitted("Only the owner can delete moderators")

        membership.delete()

        return ok({'message': "Member deleted"})

    def get(self, request, profile, membership):
        request_membership = Membership.objects.get(user=profile.user)

        if not request_membership.moderator:
            return not_permitted("Only moderators can view members")

        return ok({'member': MembershipSerialiser.serialise(membership)})
