from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.survey_item import SurveyItem
from backend.models.survey import Survey
from backend.serialisers.survey_item_serialiser import SurveyItemSerialiser
from backend.tools.decorators import Attach, attach_profile, login_required

from backend.tools.response_tools import (
    created,
    ok,
    accepted
)

@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
class SingleSurveyItemView(View):
    @method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'))
    @method_decorator(Attach.incoming('survey_item_id').to(SurveyItem).as_outgoing('survey_item'))
    def get(self, request, profile, survey, survey_item):
        return ok({
            'survey_item': SurveyItemSerialiser.serialise(survey_item)
        })

    @method_decorator(csrf_exempt)
    @method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'))
    @method_decorator(Attach.incoming('survey_item_id').to(SurveyItem).as_outgoing('survey_item'))
    def patch(self, request, profile, survey, survey_item):
        return accepted({
            'survey_item': SurveyItemSerialiser.serialise(survey_item)
        })

    @method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'))
    @method_decorator(Attach.incoming('survey_item_id').to(SurveyItem).as_outgoing('survey_item'))
    def delete(self, request, profile, survey_id, survey_item):
        return accepted({
            'message': f"Survey item {survey_item.id} has been deleted"
        })