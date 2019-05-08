class SettingSerialiser:
    @staticmethod
    def serialise(setting) -> dict:
        return {
            'key': setting.key,
            'value': setting.value
        }
