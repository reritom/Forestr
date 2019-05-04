from django.contrib import admin

from backend.models.organisation import Organisation
from backend.models.survey import Survey
from backend.models.profile import Profile
from backend.models.survey_item import SurveyItem

# Register your models here.

admin.site.register(Organisation)
admin.site.register(Survey)
admin.site.register(Profile)
admin.site.register(SurveyItem)
