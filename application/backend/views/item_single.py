from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.item import Item
from backend.serialisers.item_serialiser import ItemSerialiser
from backend.tools.decorators import Attach, attach_profile, login_required

from backend.tools.model_tools import (
    is_item_external_id_unique_to_organisation
)

from backend.tools.response_tools import (
    created,
    ok,
    accepted,
    conflict
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
class SingleItemView(View):
    @method_decorator(Attach.incoming('item_id').to(Item).as_outgoing('item'))
    def get(self, request, profile, item):
        return ok({
            'item': ItemSerialiser.serialise(item)
        })

    @method_decorator(Attach.incoming('item_id').to(Item).as_outgoing('item'))
    def patch(self, request, profile, item):
        # Check if this item already exists for the organisation or profile
        if request.POST.get('external_id'):
            if not is_item_external_id_unique_to_organisation(external_id, profile.organisation):
                conflict("There is already an item with this id linked to your organisation")

        return accepted({
            'item': ItemSerialiser.serialise(item)
        })

    @method_decorator(Attach.incoming('item_id').to(Item).as_outgoing('item'))
    def delete(self, request, profile, item):
        return accepted({
            'message': f"Item {item.id} has been deleted"
        })
