class SurveyItemSerialiser:
    @staticmethod
    def serialise(survey_item) -> dict:
        return {
            'id': survey_item.id,
            'created': survey_item.created,
            'notes': survey_item.notes
        }
