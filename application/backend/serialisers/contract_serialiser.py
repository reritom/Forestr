class ContractSerialiser:
    @staticmethod
    def serialise(contract) -> dict:
        return {
            'created': contract.created,
            'type': contract.contract_type,
            'id': contract.id,
            'status': contract.status
        }
