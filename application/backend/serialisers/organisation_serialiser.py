class OrganisationSerialiser:
    @staticmethod
    def serialise(organisation) -> dict:
        return {
            'id': organisation.id,
            'name': organisation.name,
            'description': organisation.description
        }
