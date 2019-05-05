class ProfileSerialiser:
    @staticmethod
    def serialise(profile) -> dict:
        return {
            'username': profile.user.username,
            'email': profile.user.email
        }

    @staticmethod
    def serialise_with_organisation(profile) -> dict:
        return {
            'username': profile.user.username,
            'email': profile.user.email,
            'organisation': {
                'id': profile.organisation.id,
                'name': profile.organisation.name
            }
        }
