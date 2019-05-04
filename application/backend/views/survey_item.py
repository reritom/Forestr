from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.survey_item import SurveyItem
from backend.models.survey import Survey
from backend.serialisers.survey_item_serialiser import SurveyItemSerialiser
from backend.tools.decorators import Attach

from backend.tools.response_tools import (
    created,
    ok,
    accepted
)

@method_decorator(login_required, name="dispatch")
class SurveyItemView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'))
    def post(self, request, survey):
        survey_item = SurveyItem.make(
            survey=survey,
            description=description
        )

        return created({
            'survey_item': SurveyItemSerialiser.serialise(survey_item)
        })

    @method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'))
    def get(self, request, survey):
        return ok({
            'survey_item': SurveyItemSerialiser.serialise(survey_item)
        })
