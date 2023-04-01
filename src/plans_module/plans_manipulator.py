import sys
import os
import datetime
from datetime import date
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/")

import uuid
from db import DBManipulator

class PlansManipulator:
    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def create_plan(cls, data):
        data["plan_id"] = uuid.uuid4().hex
        result = DBManipulator.insert_table("plans",[data])
        if result  == True:
            output = {"status":result,"data":{"plan_id":data["plan_id"]}}
        else:
            output = {"status":result["status"], "data":result["data"]}
        return output

    @classmethod
    def get_all_plans(cls):
        result = DBManipulator.select_query("plans")
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def get_plans(cls, plan_id):
        result = DBManipulator.select_query("plans", {"$and":[{ "plan_id":plan_id}]})
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def edit_plans(cls, data, unique_value):
        del data["unique_value"]
        result = DBManipulator.update_row("plans", [data], unique_value)
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def delete_row(cls, key, value):
        result = DBManipulator.delete_row("plans",key,value)
        return {"status" : result["status"], "data":result["data"]}

