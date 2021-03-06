from backend.models.survey_item import SurveyItem
from backend.serialisers.survey_item_serialiser import SurveyItemSerialiser

class SurveySerialiser:
    @staticmethod
    def serialise(survey) -> dict:
        survey_items = SurveyItem.objects.filter(survey=survey)

        return {
            'id': survey.id,
            'created': survey.created,
            'description': survey.description,
            'type': survey.survey_type,
            'survey_items': [
                SurveyItemSerialiser.serialise(survey_item)
                for survey_item
                in survey_items
            ]
        }
