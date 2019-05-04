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
class ItemView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, profile):
        item = Item.make(
            description=request.POST.get('description'),
            external_id=request.POST.get('external_id'),
            tags=request.POST.get('tags'),
            photos=request.POST.get('photos')
        )

        return created({
            'item': ItemSerialiser.serialise(item)
        })

    def get(self, request, profile):
        items = Item.objects.filter(profile=profile)

        return ok({
            'items': [
                ItemSerialiser.serialise(item)
                for item in items
            ]
        })
