import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/branch_module")
from ..flow.branch_flow  import BranchFlow

class BranchCore:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_branch(cls, data):
        return BranchFlow.branch_handeler("create", data)

    @classmethod
    def edite_branch(cls, data):
        return BranchFlow.branch_handeler("update",data, data["branch_code"])

    @classmethod
    def get_branch(cls, data):
        #TODO data["user_id"], data["branch_code"]
        return BranchFlow.branch_handeler("select", data)

    @classmethod
    def get_all_branch(cls, data):
        #TODO data["user_id"]
        return BranchFlow.branch_handeler("select_all", data)

    @classmethod
    def delete_branch(cls, data):
        #TODO data["user_id"]
        return BranchFlow.branch_handeler("delete", data["key"], data["value"])
