class ProfileSerialiser:
    @staticmethod
    def serialise(profile) -> dict:
        serialised = {
            'username': profile.user.username,
            'email': profile.user.email
        }

        if profile.organisation:
            serialised['organisation'] = {
                'id': profile.organisation.id,
                'name': profile.organisation.name
            }

        return serialised
