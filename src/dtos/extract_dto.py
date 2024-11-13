from models.extracts_entity import Extracts
from typing import List

class ExtractsDTO:
    @staticmethod
    def obj_to_dict(Extracts: Extracts) -> dict:
        extracts_dto = {
            "extract_key":Extracts.id,
            "agency_number":Extracts.agency_number,
            "account_number":Extracts.account_number,
            "start_date": Extracts.start_date,
            "end_date": Extracts.end_date,
            "last_transaction_datetime": str(Extracts.last_transaction_datetime)
        }
        return extracts_dto

    @staticmethod
    def list_obj_to_list_dict(sample_entities_list: List[Extracts]) -> dict:
        sample_entities_dict_list = []
        for asset in sample_entities_list:
            sample_entities_dict_list.append(ExtractsDTO.obj_to_dict(asset))
        return sample_entities_dict_list
