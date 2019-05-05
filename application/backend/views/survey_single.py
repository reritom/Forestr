from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.survey import Survey
from backend.serialisers.survey_serialiser import SurveySerialiser
from backend.tools.decorators import Attach, login_required, attach_profile, Assert

from backend.tools.response_tools import (
    created,
    ok,
    accepted
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
@method_decorator(Attach.incoming('survey_id').to(Survey).as_outgoing('survey'), name="dispatch")
@method_decorator(Assert.that('survey.organisation').equals('profile.organisation'), name="dispatch")
class SingleSurveyView(View):
    def get(self, request, profile, survey):
        return ok({'survey': SurveySerialiser.serialise(survey)})

    def patch(self, request, profile, survey):
        return accepted({'survey': SurveySerialiser.serialise(survey)})

    def delete(self, request, profile, survey):
        return accepted({'message': f"Survey {survey.id} has been deleted"})
