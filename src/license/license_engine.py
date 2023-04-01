from builtins import print
import sys
import os
import datetime
from datetime import date
import time
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append("/home/frontend/the_accountant/src")

import uuid
from db import DBManipulator

class LicenseManipulator:
    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def calculate_days(cls, number_of_days):
        start_date = date.today()
        start_date = start_date.strftime("%d/%m/%Y")
        date_1 = datetime.datetime.strptime(start_date, "%d/%m/%Y")
        end_date = date_1 + datetime.timedelta(days=number_of_days)
        date_1 = date_1.strftime("%d/%m/%Y")
        end_date = end_date.strftime("%d/%m/%Y")
        return {"start_date":start_date, "end_date":end_date}

    @classmethod
    def create_license(cls, data):
        data["license_id"] = uuid.uuid4().hex
        plan_data = DBManipulator.select_query("plans", {"plan_id":data["plan_id"]})
        if plan_data.get("data"):
            if plan_data["status"] == True:
                duration = int(plan_data["data"][0]["plan_duration"])
                data["plan_name"] = plan_data["data"][0]["plan_name"]
                data["end_date"] = cls.calculate_days(duration)["end_date"]
                data["start_date"] = cls.calculate_days(duration)["start_date"]

                result = DBManipulator.insert_table("license",[data])
                if result == True:
                    output = {"status":result,"data":{"license_id":data["license_id"]}}
                else:
                    output = {"status":result["status"], "data":result}
                return output
            else:
                return {"status":False, "data":"can't find plan name please check plan names !!"}
        else:
            return {"status":False, "data":"can't find plan name please check plan names !!"}

    @classmethod
    def get_all_license(cls, user_id = ""):
        users = {}
        result = DBManipulator.select_query("license")
        size = len(result["data"])
        for i in range(size):
            user_data = DBManipulator.select_query("user", {"user_id":result["data"][i]["user_id"]})
            if user_data.get("data"):
                users = {}
                users["user_email"] = user_data["data"][0]["email"]
                users["user_tax_number"] = user_data["data"][0]["tax_number"]
                users["user_name"] = user_data["data"][0]["name"]
                result["data"][i]["user"] =  users

        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def get_license(cls, license_id):
        result = DBManipulator.select_query("license", { "license_id":license_id})
        if result.get("data"):
            if result.get("data"):
                user_result = DBManipulator.select_query("user", {"user_id":result["data"][0]["user_id"]})
                result["data"][0]["user_id"] = user_result["data"][0]["user_id"]
                result["data"][0]["user_email"] = user_result["data"][0]["email"]
                result["data"][0]["user_tax_number"] = user_result["data"][0]["tax_number"]
                result["data"][0]["user_name"] = user_result["data"][0]["name"]
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def edit_license(cls, data, unique_value):
        del data["unique_value"]
        result = DBManipulator.update_row("license", [data], unique_value)
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def delete_row(cls, key, value):
        result = DBManipulator.delete_row("license",key,value)
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def check_license(cls, user_id):
        start_date = date.today()
        start_date = start_date.strftime("%d/%m/%Y")
        last_license = cls.get_all_license(user_id)["data"]
        if last_license:
            last_license = last_license[-1]
            start_date = start_date.split("/")
            last_license["end_date"] = last_license["end_date"].split("/")
            last_license["end_date"] = datetime.datetime(int(last_license["end_date"][2]), int(last_license["end_date"][1]), int(last_license["end_date"][0]))
            start_date = datetime.datetime(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            if last_license["end_date"] <= start_date:
                return {"expire":True}
            else:
                return {"expire":False}
        else:
            return {"expire":True, "error":f"No license for the user_id {user_id}" }


        #TODO get the plan name from and check the validity of the plan


# date_1 = datetime.datetime.strptime(start_date, "%d/%m/%Y")
# end_date = date_1 + datetime.timedelta(days=20)

# date_1 = date_1.strftime("%d/%m/%Y")
# end_date = end_date.strftime("%d/%m/%Y")
# if date_1 == start_date:
#     print(str(end_date).split(" ")[0])
# DBManipulator({"host":"localhost","port":27017})
# db = DBManipulator.create_session("accountant_db")

# data = {
#     "branch_name_en":"tabby",
#     "brnach_name_ar":"التابعي",
#     "user_id":"170474f5030c487c93f5296d99b4def"
# }
# print(BranchManipulator.create_branch(data))

# print(BranchManipulator.get_branch("cd5946e213ad40388182309061b3df2c", "170474f5030c487c93f59296d99b4def"))

# print(BranchManipulator.get_all_branches("170474f5030c487c93f59296d99b4def"))

# print(BranchManipulator.edit_branch(data,{"branch_code":"deb36435246143daa76a5e9b9e013fa9"}))
# print(BranchManipulator.delete_row("branch_id","babccf4b0e8041fb97d4fecee3ecfed7"))
