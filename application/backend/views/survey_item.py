from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.survey_item import SurveyItem
from backend.models.survey import Survey
from backend.models.item import Item
from backend.serialisers.survey_item_serialiser import SurveyItemSerialiser
from backend.tools.decorators import Attach

from backend.tools.response_tools import (
    created,
    ok,
    accepted,
    not_found,
    conflict
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'), name="dispatch")
class SurveyItemView(View):
    def post(self, request, survey):
        if not Item.objects.filter(id=request.POST['item_id']).exists():
            return not_found("Item for given id not found")

        item = Item.objects.get(id=request.POST['item_id'])

        if SurveyItem.objects.filter(survey=survey, item=item).exists():
            return conflict("This item has already been surveyed as part of this survey")

        survey_item = SurveyItem.make(
            survey=survey,
            item=item,
            notes=request.POST['notes']
        )

        return created({
            'survey_item': SurveyItemSerialiser.serialise(survey_item)
        })

    def get(self, request, survey):
        return ok({
            'survey_items': [
                SurveyItemSerialiser.serialise(survey_item)
                for survey_item
                in SurveyItem.objects.filter(survey=survey)
            ]
        })
