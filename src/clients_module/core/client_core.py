import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/clients_module")
from ..flow.clien_flow  import ClientFlow

class ClientCore:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_client(cls, data):
        return ClientFlow.client_handeler("create", data)

    @classmethod
    def edite_client(cls, data):
        return ClientFlow.client_handeler("update",data, data["tax_number"])

    @classmethod
    def get_client(cls, data):
        #TODO data["user_id"], data["branch_code"]
        return ClientFlow.client_handeler("select", data)

    @classmethod
    def get_all_client(cls, data):
        #TODO data["user_id"]
        return ClientFlow.client_handeler("select_all", data)

    @classmethod
    def delete_client(cls, data):
        return ClientFlow.client_handeler("delete", data["key"], data["value"])