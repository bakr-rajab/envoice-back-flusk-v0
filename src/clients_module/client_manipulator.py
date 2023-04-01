
import sys
import datetime
import json

sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/")
from db import DBManipulator
import uuid
from utilities import Helper
import pandas as pd
class ClientManipulator:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_client(cls, data):
        data["client_id"] = uuid.uuid4().hex
        if data.get("user_id"):
            result = DBManipulator.insert_table("clients",[data])
            if result  == True:
                return {"status":result, "data":{"client_id":data["client_id"]}}
            else:
                return  {"status":result["status"], "data":result}
        else:
            return {"status": False, "data":"The client has no user_id please provied a righ client !!"}

    @classmethod
    def create_client_with_import(cls, data):
        clients_dataframe = pd.DataFrame()

        success_client= []
        failed_client = []
        clients_data = Helper.read_csv_file(data["data"], data["validators"])
        if clients_data.get("status") == False:
            return clients_data
        else:
            user_values = DBManipulator.select_query("user", {"user_id":data["user_id"]})
            if user_values["data"]:
                clients_data = clients_data["data"].reset_index()  # make sure indexes pair with number of rows
                for index, row in clients_data.iterrows():
                    row["client_id"] = uuid.uuid4().hex
                    row["user_id"] = data["user_id"]
                    row = dict(row)
                    result = DBManipulator.insert_table("clients",[row])
                    if result  == True:
                        success_client.append({"client_id":row["client_id"]})
                        values_dict = {"client_id": row["client_id"], "client_name":row["client_name"], "ph_number":row["ph_number"], "email":row["email"], "tax_number":row["tax_number"],"client_code_number":row["client_code_number"], "address":row["address"] }
                        clients_dataframe = clients_dataframe.append(values_dict, ignore_index = True)
                    else:
                        if "tax_number" in result["data"]["error"]["details"]:
                            error = f'tax number {row["tax_number"]} already exist !!'
                        del row["client_id"]
                        del row["user_id"]
                        del row["_id"]
                        del row["index"]
                        failed_client.append({"faild_client":row, "error": error})
            else:
                return {"status":False, "data":f'user not with {data["user_id"]} found !!'}

            datetime_object = str(datetime.datetime.now()).replace(" ", "")
            f = open("utilities/conf/app_info.json")
            json_data = json.load(f)
            clients_dataframe.to_csv(f'/home/accountantnlu/the_accountant/data_output/{data["user_id"]}_clients_{datetime_object}.csv')
            if success_client:
                output = {"status":True, "failed_clients": failed_client, "success_clients":success_client, "file_paht":f'{json_data["application_data"]["APPLICATION_IP"]}:{json_data["application_data"]["APPLICATION_PORT"]}/api/download/home+accountantnlu+the_accountant+data_output+{data["user_id"]}_clients_{datetime_object}.csv'}
            else:
                output = {"status":True, "failed_clients": failed_client, "success_clients":success_client}
            return output

    @classmethod
    def edit_client(cls, data, unique_value):
        del data["unique_value"]
        client_data = DBManipulator.update_row("clients", [data], unique_value)
        return {"status":client_data["status"], "data":client_data["data"]}

    #TODO refactor this function
    @classmethod
    def get_client(cls, user_id,  tax_number):
        client_data = DBManipulator.select_query("clients", {"$and":[{ "tax_number":tax_number ,"user_id":user_id}]})
        return {"status":client_data["status"], "data":client_data["data"]}

    @classmethod
    def get_all_clients(cls, user_id):
        client_data = DBManipulator.select_query("clients", {"user_id":user_id})
        return {"status":client_data["status"], "data":client_data["data"], "number_of_records": len(client_data["data"])}

    @classmethod
    def delete_row(cls, key, value):
        client_data = DBManipulator.delete_row("clients",key,value)
        return {"status" : client_data["status"], "data":client_data["data"]}


# DBManipulator({"host":"localhost","port":27017})
# db = DBManipulator.create_session("accountant_db")

# # data = {
# #     "client_name": "mahmoud",
# #     "ph_number": 12212121,
# #     "email": "7oda@ismaiel.com",
# #     "tax_number": 12222223,
# #     "user_id":"170474f5030c487c93f59296d99b4def"
# # }
# # print(ClientManipulator.create_client(data))

# data = {
#     "client_name": "7oda",
#     "ph_number": 12212121,
#     "email": "7oda@ismaiel.com",
#     "tax_number": 12222223,
#     "user_id":"170474f5030c487c93f59296d99b4def"
# }
# # # print(ClientManipulator.edit_client(data, {"email": "7oda@ismaiel.com"}))
# # print(ClientManipulator.get_client("170474f5030c487c93f59296d99b4def"))
# print(ClientManipulator.get_client("170474f5030c487c93f59296d99b4def", data["email"] ,data["tax_number"] ))
