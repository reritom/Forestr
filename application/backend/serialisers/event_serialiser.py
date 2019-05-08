class EventSerialiser:
    @staticmethod
    def serialise(event) -> dict:
        return {
            'created': event.created,
            'description': event.description
        }
