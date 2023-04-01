import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/static_tables_modules")

from ..flow.static_table_flow import StaticDataFlow


class StaticTableCore:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def get_spacific_data(cls, data):
        return StaticDataFlow.static_data_handeler("select", data)

    @classmethod
    def get_all_table(cls, data):
        return StaticDataFlow.static_data_handeler("select_all", data)

    @classmethod
    def edite_static_table(cls, data):
        return StaticDataFlow.static_data_handeler("update",data, data["code"])

    @classmethod
    def delete_license(cls, data):
        return StaticDataFlow.static_data_handeler("delete",data)

