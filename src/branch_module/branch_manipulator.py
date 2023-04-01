import sys
import os
import datetime
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/")
import pandas as pd
import uuid
from db import DBManipulator
from utilities import Helper
class BranchManipulator:
    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def create_branch(cls, data):
        data["branch_code"] = uuid.uuid4().hex
        if not data.get("invoice_counter"):
            data["invoice_counter"]= 1
        result = DBManipulator.insert_table("branches",[data])

        if result  == True:
            output = {"status":result,"data":{"branch_code":data["branch_code"], "account_branch_code":data["account_branch_code"]}}
        else:
            output = {"status":result["status"], "data":result}
        return output

    @classmethod
    def create_branch_with_import(cls, data):
        branches_dataframe = pd.DataFrame()
        success_branches = []
        failed_branches = []
        branchs_data = Helper.read_csv_file(data["data"], data["validators"])
        if branchs_data.get("status") == False:
            return branchs_data
        else:
            user_values = DBManipulator.select_query("user", {"user_id":data["user_id"]})
            if user_values["data"]:
                branchs_data = branchs_data["data"].reset_index()  # make sure indexes pair with number of rows
                for index, row in branchs_data.iterrows():
                    row["branch_code"] = uuid.uuid4().hex
                    row["user_id"] = data["user_id"]
                    if "invoice_counter" in row:
                        row["invoice_counter"]= 1
                    row = dict(row)
                    result = DBManipulator.insert_table("branches",[row])
                    if result  == True:
                        success_branches.append({"branch_code":row["branch_code"], "account_branch_code":row["account_branch_code"]})
                        values_dict = {"branch_code": row["branch_code"], "branch_name_en":row["branch_name_en"], "brnach_name_ar":row["brnach_name_ar"], "invoice_counter":row["invoice_counter"], "account_branch_code":row["account_branch_code"]}
                        branches_dataframe = branches_dataframe.append(values_dict, ignore_index = True)
                    else:
                        if "branch_code" in result["data"]["error"]["details"]:
                            error = f'tax number {row["branch_code"]} already exist !!'
                        del row["branch_code"]
                        del row["user_id"]
                        del row["_id"]
                        del row["index"]
                        failed_branches.append({"failed_branches":row, "account_branch_code":data["account_branch_code"]})
            else:
                return {"status":False, "data":f'user not with {data["user_id"]} found !!'}
            datetime_object = str(datetime.datetime.now()).replace(" ", "")
            branches_dataframe.to_csv(f'/home/accountantnlu/the_accountant/data_output/{data["user_id"]}_branches_{datetime_object}.csv')
            f = open("utilities/conf/app_info.json")
            json_data = json.load(f)
            if success_branches:
                output = {"status":True, "failed_branches": failed_branches, "success_branches":success_branches, "file_paht":f'{json_data["application_data"]["APPLICATION_IP"]}:{json_data["application_data"]["APPLICATION_PORT"]}/api/download/home+accountantnlu+the_accountant+data_output+{data["user_id"]}_branches_{datetime_object}.csv'}
            else:
                output = {"status":True, "failed_branches": failed_branches, "success_branches":success_branches}
            return output


    @classmethod
    def get_all_branches(cls, user_id):
        branch_data = DBManipulator.select_query("branches", {"user_id":user_id})
        return {"status" : branch_data["status"], "data":branch_data["data"]}
    @classmethod
    def get_branch(cls, branch_code, user_id):
        branch_data = DBManipulator.select_query("branches", {"$and":[{"branch_code":branch_code, "user_id":user_id}]})
        return {"status" : branch_data["status"], "data":branch_data["data"]}


    @classmethod
    def edit_branch(cls, data, unique_value):
        del data["unique_value"]
        result = DBManipulator.update_row("branches", [data], unique_value)
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def delete_row(cls, user_id, key, value):
        result = DBManipulator.delete_type_row("branches", user_id, key,value)
        return {"status" : result["status"], "data":result["data"]}


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
