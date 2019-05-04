from backend.models.survey_item import SurveyItem
from backend.serialisers.survey_item_serialiser import SurveyItemSerialiser

class ItemSerialiser:
    @staticmethod
    def serialise(item) -> dict:
        survey_items = SurveyItem.objects.filter(item=item)

        return {
            'id': item.id,
            'created': item.created,
            'description': item.description,
            'survey_history': [
                SurveyItemSerialiser.serialise(survey_item)
                for survey_item
                in survey_items
            ]
        }
