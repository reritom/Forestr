from backend.models.organisation import Organisation
from backend.models.survey import Survey
from backend.models.profile import Profile
from backend.models.survey_item import SurveyItem
from backend.models.item import Item
from backend.models.membership import Membership

def get_surveys_of_organisation(organisation):
    profiles = Profile.objects.filter(organisation=organisation)
    surveys = []

    for profile in profiles:
        surveys_for_this_profile = Survey.objects.filter(profile=profile)
        surveys.extend(list(surveys_for_this_profile))

    return surveys

def get_profiles_of_organisation(organisation):
    return Profile.objects.filter(organisation=organisation)

def get_members_of_organisation(organisation):
    return Membership.objects.filter(organisation=organisation)

def get_items_of_organisation(organisation):
    return Item.objects.filter(organisation=organisation)

def is_item_external_id_unique_to_organisation(external_id, organisation) -> bool:
    return not Item.objects.filter(organisation=organisation, external_id=external_id).exists()
