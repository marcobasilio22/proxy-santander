from models.workspace_entity import Workspace
from typing import List

class WorkspaceDTO:
    @staticmethod
    def obj_to_dict(Workspace: Workspace) -> dict:
        workspace_dto = {
            "workspace_key":Workspace.id,
            "agency_number":Workspace.agency,
            "account_number":Workspace.account,
            "start_date": Workspace.start_date
        }
        return workspace_dto

    @staticmethod
    def list_obj_to_list_dict(sample_entities_list: List[Workspace]) -> dict:
        sample_entities_dict_list = []
        for asset in sample_entities_list:
            sample_entities_dict_list.append(WorkspaceDTO.obj_to_dict(asset))
        return sample_entities_dict_list





