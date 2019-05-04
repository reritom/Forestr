from backend.models.organisation import Organisation
from backend.models.survey import Survey
from backend.models.profile import Profile
from backend.models.survey_item import SurveyItem
from backend.models.item import Item

def get_surveys_of_organisation(organisation):
    profiles = Profile.objects.filter(organisation=organisation)
    surveys = []

    for profile in profiles:
        surveys_for_this_profile = Survey.objects.filter(profile=profile)
        surveys.extend(list(surveys_for_this_profile))

    return surveys

def get_profiles_of_organisation(organisation):
    return Profile.objects.filter(organisation=organisation)
