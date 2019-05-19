from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.survey import Survey
from backend.models.membership import Membership
from backend.serialisers.survey_serialiser import SurveySerialiser
from backend.tools.decorators import login_required
from backend.tools.form import Form

from backend.tools.response_tools import (
    created,
    ok,
    accepted
)

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class SurveyView(View):
    def post(self, request):
        form = Form.for_model(Survey).with_request(request)
        membership = Membership.objects.filter(user=request.user).first()

        survey = Survey.make(
            organisation=membership.organisation,
            description=form.description,
            survey_type=form.type,
            status=form.status or "PLANNED"
        )

        if form.survey_items:
            for survey_item in form.survey_items:
                # TODO create a survey item
                pass

        return created({'survey': SurveySerialiser.serialise(survey)})


    def get(self, request):
        membership = Membership.objects.get(user=request.user)

        return ok({
            'surveys': [
                SurveySerialiser.serialise(survey)
                for survey
                in Survey.objects.filter(organisation=membership.organisation)
            ]
        })
