from backend.models.membership import Membership

class ProfileSerialiser:
    @staticmethod
    def serialise(profile) -> dict:
        return {
            'username': profile.user.username,
            'email': profile.user.email
        }

    @staticmethod
    def serialise_with_organisation(profile) -> dict:
        membership = Membership.objects.get(user=profile.user)

        return {
            'username': profile.user.username,
            'email': profile.user.email,
            'organisation': {
                'id': membership.organisation.id,
                'name': membership.organisation.name,
                'moderator': membership.moderator
            }
        }
