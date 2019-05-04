from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.item import Item
from backend.serialisers.item_serialiser import ItemSerialiser
from backend.tools.decorators import Attach, attach_profile, login_required

from backend.tools.response_tools import (
    created,
    ok,
    accepted
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

    @method_decorator(csrf_exempt)
    @method_decorator(Attach.incoming('item_id').to(Item).as_outgoing('item'))
    def patch(self, request, profile, item):
        return accepted({
            'item': ItemSerialiser.serialise(item)
        })

    @method_decorator(Attach.incoming('item_id').to(Item).as_outgoing('item'))
    def delete(self, request, profile, item):
        return accepted({
            'message': f"Item {item.id} has been deleted"
        })
