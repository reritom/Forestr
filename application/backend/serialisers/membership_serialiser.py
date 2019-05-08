class MembershipSerialiser:
    @staticmethod
    def serialise(membership) -> dict:
        return {
            'joined': membership.joined,
            'moderator': membership.moderator,
            'id': membership.id,
            'organisation': {
                'id': membership.organisation.id
            },
            'username': membership.user.username,
            'origin': membership.origin
        }
