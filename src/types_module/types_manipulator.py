import sys
import os
import pandas as pd
import datetime
import logging
import json
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/")

from db import DBManipulator
import uuid
from utilities import Helper

# logging.basicConfig(filename="/home/accountantnlu/the_accountant/logs/inbound.log", level=logging.DEBUG,
#                     format="%(asctime)s %(message)s", filemode="w")
class TypeManipulator:
    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def create_type_group(cls, data):
        data["group_code"] = uuid.uuid4().hex
        result = DBManipulator.insert_table("types_groups",[data])
        if result  == True:
            return {"status":result, "data":{"group_code":data["group_code"]}}
        else:
            return {"status": False, "data":result}

    @classmethod
    def create_types_group_with_import(cls, data):
        types_groups_dataframe = pd.DataFrame()
        success_types_groups = []
        failed_types_groups= []
        types_groups_data = Helper.read_csv_file(data["data"], data["validators"])
        if types_groups_data.get("status") == False:
            return types_groups_data
        else:
            user_values = DBManipulator.select_query("user", {"user_id":data["user_id"]})
            if user_values["data"]:

                types_groups_data = types_groups_data["data"].reset_index()  # make sure indexes pair with number of rows
                for index, row in types_groups_data.iterrows():
                    row["group_code"] = uuid.uuid4().hex
                    row["user_id"] = data["user_id"]
                    row = dict(row)
                    result = DBManipulator.insert_table("types_groups",[row])

                    if result  == True:
                        success_types_groups.append({"group_code":row["group_code"]})
                        values_dict = {"group_code": row["group_code"], "group_name_ar":row["group_name_ar"], "group_name_en":row["group_name_en"]}
                        types_groups_dataframe = types_groups_dataframe.append(values_dict, ignore_index = True)
                    else:
                        failed_types_groups.append({"group_code":row["group_code"]})
            else:
                return {"status":False, "data":f'user not with {data["user_id"]} found !!'}
            datetime_object = str(datetime.datetime.now()).replace(" ", "")
            f = open("utilities/conf/app_info.json")
            json_data = json.load(f)
            types_groups_dataframe.to_csv(f'/home/accountantnlu/the_accountant/data_output/{data["user_id"]}_types_group_{datetime_object}.csv')
            output = {"status":True, "failed_type_groups": failed_types_groups, "success_type_groups":success_types_groups, "file_paht":f'{json_data["application_data"]["APPLICATION_IP"]}:{json_data["application_data"]["APPLICATION_PORT"]}/api/download/home+accountantnlu+the_accountant+data_output+{data["user_id"]}_types_group_{datetime_object}.csv'}
            return output

    @classmethod
    def create_types_with_import(cls, data):
        types_dataframe = pd.DataFrame()
        success_types = []
        failed_types= []
        types_data = Helper.read_csv_file(data["data"], data["validators"])
        if types_data.get("status") == False:
            return types_data
        else:
            user_values = DBManipulator.select_query("user", {"user_id":data["user_id"]})
            if user_values["data"]:
                types_data = types_data["data"].reset_index()  # make sure indexes pair with number of rows
                for index, row in types_data.iterrows():
                    row["type_code"] = uuid.uuid4().hex
                    row["user_id"] = data["user_id"]
                    if row["tax_code_type"] == "EGS":
                        user_tax_number = DBManipulator.select_query("user", {"user_id":data["user_id"]})
                        if user_tax_number["data"][0]["tax_number"]:
                            row["tax_code"] = f'EG-{user_tax_number["data"][0]["tax_number"]}-{row["tax_code"]}'
                        else:
                            return {"status":False, "data":f'user not with {data["user_id"]}found !!'}
                    else:
                        row["tax_code"] = row["tax_code"]
                    row = dict(row)
                    result = DBManipulator.insert_table("types",[row])

                    if result  == True:
                        success_types.append({"type_code":row["type_code"]})
                        values_dict = {"type_code": row["type_code"], "account_type_code":row["account_type_code"], "type_name":row["type_name"], "tax_code_type":row["tax_code_type"], "tax_code":row["tax_code"],"type_group":row["type_group"], "unit_of_measurment":row["unit_of_measurment"], "tax_type":row["tax_type"], "tax_percentage":row["tax_percentage"], "price":row["price"] }
                        types_dataframe = types_dataframe.append(values_dict, ignore_index = True)
                    else:

                        failed_types.append({"type_code":row["type_code"]})
            else:
                return {"status":False, "data":f'user not with {data["user_id"]} found !!'}
            datetime_object = str(datetime.datetime.now()).replace(" ", "")
            f = open("utilities/conf/app_info.json")
            json_data = json.load(f)
            types_dataframe.to_csv(f'/home/accountantnlu/the_accountant/data_output/{data["user_id"]}_types_{datetime_object}.csv')
            output = {"status":True, "failed_type": failed_types, "success_type":success_types, "file_paht":f'{json_data["application_data"]["APPLICATION_IP"]}:{json_data["application_data"]["APPLICATION_PORT"]}/api/download/home+accountantnlu+the_accountant+data_output+{data["user_id"]}_types_{datetime_object}.csv'}
            return output
    @classmethod
    def create_type(cls, data):
        if data.get("type_group"):
            data["type_code"] = uuid.uuid4().hex
            if data.get("tax_code_type"):
                if data["tax_code_type"] == "EGS":
                    user_tax_number = DBManipulator.select_query("user", {"user_id":data["user_id"]})
                    data["tax_code"] = f'EG-{user_tax_number["data"][0]["tax_number"]}-{data["tax_code"]}'
                else:
                    data["tax_code"] = data["tax_code"]
            result = DBManipulator.insert_table("types",[data])
            if result  == True:
                return {"status":result, "data":{"type_code":data["type_code"]}}
            else:
                return {"status": False, "data":result}
        else:
            return {"status": False, "data":"Thier is no group for this type"}
    @classmethod
    def get_type_group(cls, group_code, user_id):
        result = DBManipulator.select_query("types_groups", {"$and":[{"group_code":group_code, "user_id":user_id}]})
        return {"status":result["status"], "data":result["data"]}

    @classmethod
    def get_all_type_group(cls, user_id):
        result = DBManipulator.select_query("types_groups", {"user_id":user_id})
        return {"status":result["status"], "data":result["data"], "number_of_records":len(result["data"])}

    @classmethod
    def get_type(cls, type_code, user_id):
        result = DBManipulator.select_query("types", {"$and":[{"type_code":type_code, "user_id":user_id}]})
        return {"status":result["status"], "data":result["data"]}

    @classmethod
    def get_all_types(cls, user_id):
        result = DBManipulator.select_query("types", {"user_id":user_id})
        logging.debug('[hello] request has been done')
        return {"status":result["status"], "data":result["data"], "number_of_records":len(result["data"])}

    @classmethod
    def edit_type(cls, data, unique_value):
        del data["unique_value"]
        if data.get("tax_code_type"):
            if data["tax_code_type"] == "EGS":
                user_tax_number = DBManipulator.select_query("user", {"user_id":data["user_id"]})
                if "EG" in data["tax_code"]:
                    data["tax_code"] = data["tax_code"].split("-")
                    data["tax_code"] = f'EG-{user_tax_number["data"][0]["tax_number"]}-{data["tax_code"][2]}'
                else:
                    data["tax_code"] = f'EG-{user_tax_number["data"][0]["tax_number"]}-{data["tax_code"]}'

            else:
                if "EG" in data["tax_code"]:

                    data["tax_code"] = data["tax_code"].split("-")
                    data["tax_code"] = data["tax_code"][2]
                else:
                    data["tax_code"] = data["tax_code"]
        result = DBManipulator.update_row("types", [data], unique_value)
        return {"status":result["status"], "data":result["data"]}

    @classmethod
    def edit_types_group(cls, data, unique_value):
        del data["unique_value"]
        result= DBManipulator.update_row("types_groups", [data], unique_value)
        return {"status":result["status"], "data":result["data"]}

    @classmethod
    def delete_row(cls, table_name, user_id, key, value):
        result = DBManipulator.delete_type_row(table_name, user_id, key,value)
        return {"status" : result["status"], "data":result["data"]}


# DBManipulator({"host":"localhost","port":27017})
# db = DBManipulator.create_session("accountant_db")

# print(TypeManipulator.get_type(1,"170474f5030c487c93f59296d99b4def"))


# data = {
#     "group_name_ar": "تابلوهات",
#     "group_name_en": "tablooos",
#     "user_id": "170474f5030c487c93f59296d99b4def",
#     }
# data = {
#     "type_code":3,
#     "type_name":"tablohat",
#     "tax_code": 1231231,
#     "type_group":2,
#     "unit_of_measurment": "wa7da",
#     "tax_type":3,
#     "tax_percentage":2,
#     "price":30000,
#     "user_id":"12"
#     }
# print(TypeManipulator.edit_types_group(data,{"group_code":1}))
# print(TypeManipulator.create_type_group(data))
# print(TypeManipulator.create_type(data))
