from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.item import Item
from backend.models.membership import Membership
from backend.serialisers.item_serialiser import ItemSerialiser
from backend.tools.decorators import Attach, login_required
from backend.tools.form import Form

from backend.tools.model_tools import (
    is_item_external_id_unique_to_organisation,
    get_items_of_organisation
)

from backend.tools.response_tools import (
    created,
    ok,
    accepted,
    conflict
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class ItemView(View):
    @method_decorator(csrf_exempt)
    def post(self, request):
        form = Form.for_model(Item).with_request(request)
        membership = Membership.objects.get(user=request.user)

        if not is_item_external_id_unique_to_organisation(form.external_id, membership.organisation):
            return conflict("There is already an item with this id linked to your organisation")

        item = Item.make(
            organisation=membership.organisation,
            description=form.description,
            external_id=form.external_id,
            tags=form.tags,
            photos=form.photos
        )

        return created({'item': ItemSerialiser.serialise(item)})

    def get(self, request):
        membership = Membership.objects.get(user=request.user)
        return ok({
            'items': [
                ItemSerialiser.serialise(item)
                for item
                in get_items_of_organisation(membership.organisation)
            ]
        })
