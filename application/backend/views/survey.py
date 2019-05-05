from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.survey import Survey
from backend.serialisers.survey_serialiser import SurveySerialiser
from backend.tools.decorators import Attach, login_required, attach_profile

from backend.tools.response_tools import (
    created,
    ok,
    accepted
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
class SurveyView(View):
    def post(self, request, profile):
        survey = Survey.make(
            organisation=profile.organisation,
            description=request.POST['description'],
            survey_type=request.POST['type'],
            status=request.POST.get('status', "PLANNED")
        )

        return created({
            'survey': SurveySerialiser.serialise(survey)
        })


    def get(self, request, profile):
        return ok({
            'surveys': [
                SurveySerialiser.serialise(survey)
                for survey
                in Survey.objects.filter(organisation=profile.organisation)
            ]
        })
