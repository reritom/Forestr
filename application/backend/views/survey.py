from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.survey import Survey
from backend.serialisers.survey_serialiser import SurveySerialiser
from backend.tools.decorators import Attach, login_required, attach_profile
from backend.tools.form import Form

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
        form = Form.for_model(Survey).with_request(request)

        survey = Survey.make(
            organisation=profile.organisation,
            description=form.description,
            survey_type=form.type,
            status=form.status or "PLANNED"
        )

        return created({'survey': SurveySerialiser.serialise(survey)})


    def get(self, request, profile):
        return ok({
            'surveys': [
                SurveySerialiser.serialise(survey)
                for survey
                in Survey.objects.filter(organisation=profile.organisation)
            ]
        })
