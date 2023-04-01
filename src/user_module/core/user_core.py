import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/user_module")
from ..flow.user_flow import UserFlow

class UserCore:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_user(cls, data):
        return UserFlow.user_handeler("create",data)

    @classmethod
    def login(cls, data):
        return UserFlow.user_handeler("auth", data)

    @classmethod
    def edite_user(cls, data):
        return UserFlow.user_handeler("update",data, data["tax_number"])

    @classmethod
    def delete_user(cls, data):
        return UserFlow.user_handeler("delete",data)

    @classmethod
    def get_user(cls, data):
        return UserFlow.user_handeler("select", data)

    @classmethod
    def get_all_user(cls):
        return UserFlow.user_handeler("select_all")

# data = {"user_id":"a6ba97cb8ab34ec19284f1ceaa9e2a98"}

# print(UserCore.get_user(data))