from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.survey import Survey
from backend.serialisers.survey_serialiser import SurveySerialiser
from backend.tools.decorators import Attach, login_required

from backend.tools.response_tools import (
    created,
    ok,
    accepted
)

@method_decorator(login_required, name="dispatch")
class SingleSurveyView(View):
    @method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'))
    def get(self, request, survey):
        return ok({
            'survey': SurveySerialiser.serialise(survey)
        })

    @method_decorator(csrf_exempt)
    @method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'))
    def patch(self, request, survey):
        return accepted({
            'survey': SurveySerialiser.serialise(survey)
        })

    @method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'))
    def delete(self, request, survey):
        return accepted({
            'message': f"Survey {survey.id} has been deleted"
        })
