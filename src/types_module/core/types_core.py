import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/types_module")
from ..flow import TypesFlow


class TypesCore:

    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_types(cls, data):
        return TypesFlow.types_handeler("create", data)

    @classmethod
    def edite_types(cls, data):
        return TypesFlow.types_handeler("update",data, data["type_code"])

    @classmethod
    def get_types(cls, data):
        return TypesFlow.types_handeler("select", data)

    @classmethod
    def get_all_types(cls, data):
        #TODO data["user_id"]
        return TypesFlow.types_handeler("select_all", data)

    @classmethod
    def delete_types(cls, data):
        return TypesFlow.types_handeler("delete", data["key"], data["value"])
