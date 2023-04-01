
import sys
from db import DBManipulator
from src.license import LicenseManipulator
from src.static_tables_modules import StaticTables
from passlib.hash import pbkdf2_sha256
import uuid

class User:
    def __init__(self) -> None:
        pass

    @classmethod
    def get_user(cls, user_id):
        user_data = DBManipulator.select_query("user", {"user_id":user_id})
        if user_data.get("data"):
            if user_data["status"] == True:
                del user_data["data"][0]["password"]
        else:
            user_data["status"]= False
            user_data["data"] = {
                "errors":{
                    "status":False,
                    "title":"No user found",
                    "msg":f"No type added with this  user id {user_id}"
                }
            }
        return {"status":user_data["status"], "data":user_data["data"]}

    @classmethod
    def get_all_users(cls):
        user_data = DBManipulator.select_query("user")
        users_list = []
        if user_data.get("data"):
            if user_data["status"] == True:
                for i in range(len(user_data["data"])):
                    if user_data["data"][i]["user_role"] =="user":
                        users_list.append(user_data["data"][i])
                return {"status":True, "data":users_list, "number_of_records":len(users_list)}
            elif user_data["status"] == False:
                return {"status":False, "data":user_data["data"]}
        else:
            user_data["status"]= False
            user_data["data"] = {
                "errors":{
                    "status":False,
                    "title":"No users found",
                    "msg":f"No users found"
                }
            }

        return {"status":False, "data":user_data["data"]}

    @classmethod
    def authinticate_user(cls,  tax_number, password):
        user_data = DBManipulator.select_query("user", {"tax_number":tax_number})
        if user_data.get("data"):
            if user_data["status"] == False:
                output = {"status":False}
            else:
                if user_data["data"][0]["tax_number"] == tax_number and pbkdf2_sha256.verify(password, user_data["data"][0]["password"]):
                    del user_data["data"][0]["password"]
                    if user_data["data"][0]["user_role"] == "admin":
                        output = {"status":True , "data":user_data["data"]}
                        return output
                    data = LicenseManipulator.check_license(user_data["data"][0]["user_id"])
                    if data.get("error"):
                        output = {"status":True , "data":data["error"],"expire":data["expire"]}
                    else:
                        # StaticTables.check_is_tables(user_data["data"][0]["user_id"])

                        output = {"status":True , "data":user_data["data"],"expire":data["expire"]}
                else:
                    output = {"status":False, "data":"not autinticated"}
        else:
            output = {"status":False, "data":"not autinticated"}

        return output

    @classmethod
    def create_user(cls,  data):
        data["user_id"] = uuid.uuid4().hex
        data['password'] = pbkdf2_sha256.hash(data['password'])
        data["user_role"] = "user"
        result = DBManipulator.insert_table("user",[data])
        if result == True:
            del data["password"]
            del data["_id"]
            output = {"status":True, "data":data}
        else:
            output = {"status":False, "data":result}
        return output

    @classmethod
    def edite_user(cls, data, unique_value):
        del data["unique_value"]
        if data.get("password"):
            data['password'] = pbkdf2_sha256.hash(data['password'])
        result = DBManipulator.update_row("user", [data], unique_value)
        if result["status"] == True:
            output = {"status": True,"data":data}
        else:
            output = {"status":False, "data":result}
        return output

    @classmethod
    def delete_row(cls, key, value):
        result = DBManipulator.delete_row("user",key,value)
        if result == True:
            output = {"status":True, "data":{key:value}}
        else:
            output = {"status":False, "data":result}
        return output

# DBManipulator({"host":"localhost","port":27017})
# db = DBManipulator.create_session("accountant_db")
# print(User.get_all_users()[0])
# data_user = User.get_user("170474f5030c487c93f59296d99b4def")
# print(data_user[0]["name"])
# # print(data_user[0]["email"])

# # print(User.authinticate_user("mahmoud.hamdy@istnetworks.com","1345"))
# data = {
#     "user_id":12,
#     "name":"mahmoud",
#     "ph_number":112154224,
#     "email":"7oda@istnetworks.com",
#     "password":"1345",
#     "tax_num":112232222,
#     "activity_code":999,
#     "adress":"9-fil sr",
#     "token_one":"1212",
#     "token_two":"3333"
# }
# print(User.edite_user(data, {"email":"mahmoud.hamdy@istnetworks.com"}))
# print(User.create_user( data))