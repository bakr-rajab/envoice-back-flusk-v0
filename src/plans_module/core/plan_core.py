import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/license/")
from ..flow import PlansFlow


class PlansCore:

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def create_plan(cls, data):
        return PlansFlow.plan_handeler("create", data)

    @classmethod
    def edite_plan(cls, data):
        return PlansFlow.plan_handeler("update",data, data["unique_value"]["plan_id"])

    @classmethod
    def get_plan(cls, data):
        return PlansFlow.plan_handeler("select", data)

    @classmethod
    def get_all_plan(cls, data):
        #TODO data["user_id"]
        return PlansFlow.plan_handeler("select_all", data)

    @classmethod
    def delete_plan(cls, data):
        return PlansFlow.plan_handeler("delete", data["key"], data["value"])

