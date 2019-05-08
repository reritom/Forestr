from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.item import Item
from backend.models.membership import Membership
from backend.serialisers.item_serialiser import ItemSerialiser
from backend.tools.decorators import Attach, Assert, login_required
from backend.tools.form import Form

from backend.tools.model_tools import (
    is_item_external_id_unique_to_organisation
)

from backend.tools.response_tools import (
    ok,
    accepted,
    conflict,
    not_permitted
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(Attach.incoming('item_id').to(Item).as_outgoing('item'), name="dispatch")
class SingleItemView(View):
    def get(self, request, item):
        membership = Membership.objects.get(user=request.user)
        if not item.organisation == membership.organisation:
            return not_permitted("This item doesn't belong to your organisation")

        return ok({'item': ItemSerialiser.serialise(item)})

    def patch(self, request, item):
        form = Form.for_model(Item).with_request(request)
        membership = Membership.objects.get(user=request.user)

        # Check if this item already exists for the organisation or profile
        if form.external_id:
            if not is_item_external_id_unique_to_organisation(form.external_id, membership.organisation):
                return conflict("There is already an item with this id linked to your organisation")

            item.set_external_id(form.external_id)

        return accepted({'item': ItemSerialiser.serialise(item)})

    def delete(self, request, item):
        return accepted({'message': f"Item {item.id} has been deleted"})
