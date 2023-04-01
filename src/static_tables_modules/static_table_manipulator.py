import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
DIR_PATH = os.path.dirname(os.path.realpath(__file__)).replace("flow","")
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/")

import uuid
from db import DBManipulator
from utilities import Helper

class StaticTables:
    @classmethod
    def __init__(cls):
        pass
    @classmethod
    def check_is_tables(cls, table_name, user_id):
        result = DBManipulator.select_query(table_name, {"user_id":user_id})
        if result.get("data"):
            if result["status"] == True:
                return {"status":True, "details": "the tables already exist."}
            else:
                cls.create_table(os.path.join(DIR_PATH,"docs"), user_id)
                return {"status": True, "details":"the tables created."}

    @classmethod
    def create_table(cls, root_dir):
        if os.path.isdir(root_dir):
            data, keys = Helper.read_files(root_dir)
            for table_name in data:
                DBManipulator.insert_table(table_name, data[table_name])
            return {"data":True}
        else:
            return {"data":False}

    @classmethod
    def edit_static_table(cls, table_name ,data, unique_value):
        del data["unique_value"]
        result = DBManipulator.update_row(table_name, [data], unique_value)
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def delete_row(cls, table_name, key, value):
        result = DBManipulator.delete_row(table_name,key,value)
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def get_all_table(cls, table_name):
        result = DBManipulator.select_query(table_name)
        if result.get("data"):
            if result["status"] == True:
                return {"status": result["status"], "data" :result["data"], "number_of_records": len(result["data"])}
            else:
                return {"status": result["status"], "data" :result["data"]}

    @classmethod
    def get_table_with_id(cls, table_name, code):
        result = DBManipulator.select_query(table_name, {"code":code})
        if result["status"] == True:
            return {"status": result["status"], "data" :result["data"], "number_of_records": len(result["data"])}


