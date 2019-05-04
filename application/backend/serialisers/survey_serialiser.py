class SurveySerialiser:
    @staticmethod
    def serialise(survey) -> dict:
        return {
            'id': survey.id,
            'created': survey.created,
            'description': survey.description
        }
