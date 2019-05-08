from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.organisation import Organisation
from backend.models.membership import Membership
from backend.models.contract import Contract
from backend.serialisers.organisation_serialiser import OrganisationSerialiser
from backend.tools.decorators import Attach, attach_profile, login_required
from backend.tools.form import Form

from backend.tools.response_tools import (
    conflict,
    created,
    ok,
    accepted,
    not_permitted,
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class OrganisationView(View):
    def post(self, request):
        form = Form.for_model(Organisation).with_request(request)
        membership = Membership.objects.get(user=request.user)

        if membership.organisation.enterprise:
            return conflict("User already part of an organisation")

        if Organisation.objects.filter(name=form.name).exists():
            return conflict(f"Organisation name {form.name} taken")

        if Organisation.objects.filter(owner=request.user, enterprise=True).exists():
            return conflict("User already owner of organisation")

        organisation = Organisation.make(
            name=form.name,
            description=form.description,
            founder=request.user,
            owner=request.user,
            enterprise=True,
            personal=False
        )

        membership.delete()
        new_membership = Membership.make(
            user=request.user,
            organisation=organisation,
            moderator=True,
            confirmed=True,
            origin=Membership.ORIGIN_OWNER
        )

        return created({'organisation': OrganisationSerialiser.serialise(organisation)})

    def patch(self, request):
        membership = Membership.objects.get(user=request.user)

        if not membership.is_owner:
            return not_permitted("Only owners can update the organisation")

        form = Form.for_model(Organisation).with_request(request)

        # Change the name
        if form.new_name:
            membership.organisation.change_name(form.new_name)

        # Change owner
        if form.new_owner:
            # Get the account for that user
            if not User.objects.filter(username=form.new_owner).exists():
                return not_found(f"User {form.new_owner} doesn't exist")

            new_owner_user = User.objects.get(username=form.new_owner)

            # Check they are a member of this organisation
            if not Membership.objects.filter(user=new_owner_user, organisation=organisation).exists():
                return not_found(f"User {form.new_owner} needs to be part of the organisation before becoming owner")

            new_owner_membership = Membership.objects.get(user=new_owner_user, organisation=organisation)

            if new_owner_membership.moderator:
                # Create the contract
                contract = Contract.make(
                    contract_type=Contract.OWNERSHIP_TRANSFER,
                    organisation=membership.organisation,
                    user=new_owner_user
                )
            else:
                return not_permitted("Only moderators can be transferred ownership")

        return accepted({'organisation': OrganisationSerialiser.serialise(organisation)})

    def get(self, request):
        membership = Membership.objects.get(user=request.user)
        return ok({'organisation': OrganisationSerialiser.serialise(membership.organisation)})

    def delete(self, request):
        #TODO Only owners of enterprise organisations can delete the organisation (requires email confirmation)
        # On confirmation, all profiles are returned to their personal organisation
        return accepted({'message': f"organisation has been deleted"})
