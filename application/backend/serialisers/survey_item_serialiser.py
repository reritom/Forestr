class SurveyItemSerialiser:
    @staticmethod
    def serialise(survey_item) -> dict:
        return {
            'id': survey.id,
            'created': survey.created,
            'description': survey.description
        }
