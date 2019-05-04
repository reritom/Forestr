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

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class SurveyView(View):
    def post(self, request):
        survey = Survey.make(
            description=request.POST['description'],
            survey_type=request.POST['type']
        )

        return created({
            'survey': SurveySerialiser.serialise(survey)
        })


    def get(self, request):
        surveys = Survey.objects.filter(user=request.user)

        return ok({
            'surveys': [
                SurveySerialiser.serialise(survey)
                for survey
                in surveys
            ]
        })
