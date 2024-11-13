from models.balance_entity import Balance
from typing import List

class BalanceDTO:
    @staticmethod
    def obj_to_dict(Balance: Balance) -> dict:
        balance_dto = {
            "account_key":Balance.id,
            "account_number":Balance.account_number,
            "account_branch":Balance.agency_number,
            "balance_value": Balance.balance_value,
            "last_transaction_datetime": str(Balance.last_transaction_datetime)
        }
        return balance_dto

    @staticmethod
    def list_obj_to_list_dict(sample_entities_list: List[Balance]) -> dict:
        sample_entities_dict_list = []
        for asset in sample_entities_list:
            sample_entities_dict_list.append(BalanceDTO.obj_to_dict(asset))
        return sample_entities_dict_list
