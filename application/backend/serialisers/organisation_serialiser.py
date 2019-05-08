from backend.models.setting import Setting
from backend.serialisers.setting_serialiser import SettingSerialiser

class OrganisationSerialiser:
    @staticmethod
    def serialise(organisation) -> dict:
        return {
            'id': organisation.id,
            'name': organisation.name,
            'description': organisation.description,
            'enterprise': organisation.enterprise,
            'personal': organisation.personal,
            'publicly_searchable': organisation.publicly_searchable
        }

    @staticmethod
    def serialise_with_settings(organisation) -> dict:
        serialised = OrganisationSerialiser.serialise(organisation)
        serialised.update({
            'settings': [
                SettingSerialiser.serialise(setting)
                for setting
                in Setting.objects.filter(organisation=organisation)
            ]
        })
