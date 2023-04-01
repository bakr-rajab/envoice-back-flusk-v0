
from builtins import print
from glob import escape
from importlib.resources import path
import re
import sys
import os
import json
import pandas as pd
from zipfile import ZipFile
import datetime
import httpx
from decouple import config
# dir_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/")

import uuid
from db import DBManipulator
from utilities import Helper
from src.types_module import TypeManipulator
from src.branch_module import BranchManipulator
from src.clients_module import ClientManipulator
from src.static_tables_modules import StaticTables
from src.user_module import User
class InvoiceManipulator:

    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def get_invoices_branch(cls, branch, user_id):
        result = DBManipulator.select_query("invoice", {"$and":[{"branch":branch, "user_id":user_id}]})
        if result.get("data"):
            last_invoice = result["data"][-1]
            return last_invoice
        else:
            return {}

    @classmethod
    def create_invoice_or_report_or_type(cls, table_name, unique_key ,data):
        data[unique_key] = uuid.uuid4().hex
        data["sent_lable"] = False
        # pending, not_sent, accepted, rejected
        data["invoice_status"] = "not_sent"
        data["invoice_url"] = "not_sent"
        data["invoice_uuid"] = "not_sent"
        data["invoice_send_time"] = "not_sent"


        if table_name == "invoice":
            last_invoice_branch = cls.get_invoices_branch(data["branch"],data["user_id"])
            if last_invoice_branch:
                data["invoice_counter"] = int(last_invoice_branch["invoice_counter"]) + 1
            else:
                branch_data = BranchManipulator.get_branch(data["branch"],data["user_id"])
                if branch_data:
                    data["invoice_counter"]  = branch_data["data"][0]["invoice_counter"]
            if data["date"]:
                date_arr = data["date"]
                time = datetime.datetime.now().strftime('%H:%M:%S')
                data["date"] = f'{data["date"]}T{time}Z'
        result = DBManipulator.insert_table(table_name,[data])
        if result  == True:
            if data.get("invoice_counter"):
                return {"status":result, "data":{unique_key:data[unique_key], "invoice_counter":data["invoice_counter"]}}
            else:
                return {"status":result, "data":{unique_key:data[unique_key]}}
        else:
            return {"status": False, "data":result}

    @classmethod
    def create_invoice_types_with_import(cls, data):
        invoice_types_dataframe = pd.DataFrame()
        success_invoice_types = []
        failed_invoice_types= []
        invoice_types_data = Helper.read_csv_file(data["data"], data["validators"])
        if invoice_types_data.get("status") == False:
            return invoice_types_data
        else:
            invoice_types_data = invoice_types_data["data"].reset_index()  # make sure indexes pair with number of rows
            for index, row in invoice_types_data.iterrows():
                row["user_id"] = data["user_id"]
                row["invoice_type_code"] = uuid.uuid4().hex
                row = dict(row)
                result = DBManipulator.insert_table("invoice_type",[row])

                if result  == True:
                    success_invoice_types.append({"invoice_type_code":row["invoice_type_code"]})
                    values_dict = {"invoice_type_code": row["invoice_type_code"], "total_money_type":row["total_money_type"], "amount":row["amount"], "invoice_type_id":row["invoice_type_id"], "type_tax_percentage":row["type_tax_percentage"], "type_added_tax":row["type_added_tax"], "type_comm_tax":row["type_comm_tax"], "type_comm_ratio":row["type_comm_ratio"]}
                    invoice_types_dataframe = invoice_types_dataframe.append(values_dict, ignore_index = True)
                else:
                    if "invoice_type_code" in result["data"]["error"]["details"]:
                        error = f'tax number {row["invoice_type_code"]} already exist !!'
                    del row["invoice_code"]
                    del row["user_id"]
                    del row["_id"]
                    del row["index"]
                    failed_invoice_types.append({"invoice_type_code":row, "error":error})
            datetime_object = datetime.datetime.now().replace(" ", "")
            f = open("utilities/conf/app_info.json")
            json_data = json.load(f)
            invoice_types_dataframe.to_csv(f'/home/accountantnlu/the_accountant/data_output/{data["user_id"]}_invoice_types_{datetime_object}.csv')
            output = {"status":True, "failed_type_groups": failed_invoice_types, "success_type_groups":success_invoice_types, "file_paht":f'{json_data["application_data"]["APPLICATION_IP"]}:{json_data["application_data"]["APPLICATION_PORT"]}/api/download/home+accountantnlu+the_accountant+data_output+{data["user_id"]}_invoice_types_{datetime_object}.csv'}
            return output


    @classmethod
    def create_invoice_with_import(cls, data):
        success_invoice = []
        failed_invoice= []
        invoice_data = Helper.read_csv_file(data["data"], data["validators"])
        if invoice_data.get("status") == False:
            return invoice_data
        else:
            user_values = DBManipulator.select_query("user", {"user_id":data["user_id"]})
            if user_values["data"]:
                invoice_data = invoice_data["data"].reset_index()  # make sure indexes pair with number of rows
                for index, row in invoice_data.iterrows():
                    if not row["date"]:
                        row["date"] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                    row["user_id"] = data["user_id"]
                    row["invoice_code"] = uuid.uuid4().hex
                    row["sent_lable"] = False
                    last_invoice_branch = cls.get_invoices_branch(row["branch"],row["user_id"])
                    if last_invoice_branch:
                        row["invoice_counter"] = int(last_invoice_branch["invoice_counter"]) + 1
                    else:
                        branch_data = BranchManipulator.get_branch(row["branch"],row["user_id"])
                        if branch_data:
                            row["invoice_counter"]  = branch_data["data"][0]["invoice_counter"]
                    row = dict(row)
                    result = DBManipulator.insert_table("invoice",[row])

                    if result  == True:
                        success_invoice.append({"invoice_code":row["invoice_code"]})
                    else:
                        if "invoice_code" in result["data"]["error"]["details"]:
                            error = f'tax number {row["invoice_code"]} already exist !!'
                        del row["invoice_code"]
                        del row["user_id"]
                        del row["_id"]
                        del row["index"]
                        failed_invoice.append({"failed_invoice":row, "error":error})
            else:
                return {"status":False, "data":f'user not with {data["user_id"]} found !!'}
            output = {"status":True, "failed_invoices": failed_invoice, "success_invoices":success_invoice}
            return output


    @classmethod
    def get_specific_invoices_types(cls, invoice_type_code, user_id):
        all_invoice_types = []
        if invoice_type_code:
            for i in invoice_type_code:
                result = DBManipulator.select_query("invoice_type", {"$and":[{"invoice_type_code":i, "user_id":user_id}]})
                if result.get("data"):
                    type_value = result["data"][0]["invoice_type_id"]
                    type_data = TypeManipulator.get_type(type_value, user_id)
                    type_data["data"][0]["type_group"] = TypeManipulator.get_type_group(type_data["data"][0]["type_group"], user_id)["data"]
                    result["data"][0]["invoice_type_id"] = type_data["data"]
                    all_invoice_types.append(result["data"][0])
                else:
                    result["status"] = False
                    result["data"] = {
                        "errors":{
                            "status":False,
                            "title":"No invoice type found",
                            "msg":f"No type added with this  invoice_type_code {invoice_type_code}"
                        }
                    }
                    return {"status":result["status"], "data":result}
            return {"status":result["status"], "data":all_invoice_types}
        else:
            return {"status":False, "data":all_invoice_types}


    @classmethod
    def get_all_invoices(cls, user_id):
        result = DBManipulator.select_query("invoice", {"user_id":user_id})
        for element in result["data"]:
            branch = BranchManipulator.get_branch(element["branch"], user_id)
            if branch.get("data"):
                branch_name = branch["data"][0]["brnach_name_ar"]
                result["data"][result["data"].index(element)]["branch_name"] = branch_name
            client = ClientManipulator.get_client(user_id, element["client"])
            if client.get("data"):
                client_tax_number = client["data"][0]["tax_number"]
                client_name = client["data"][0]["client_name"]
                result["data"][result["data"].index(element)]["client"] = client_name
                result["data"][result["data"].index(element)]["client_tax_number"] = client_tax_number


        return {"status":result["status"], "data":result["data"], "number_of_records": len(result["data"])}

    @classmethod
    def get_all_invoices_reports(cls, user_id):
        result = DBManipulator.select_query("invoice_report", {"user_id":user_id})
        for element in result["data"]:
            print(DBManipulator.select_query("invoice_report", {"report_code":element["report_code"]}))
            branch = BranchManipulator.get_branch(element["branch"], user_id)
            if branch.get("data"):
                branch_name = branch["data"][0]["brnach_name_ar"]
                result["data"][result["data"].index(element)]["branch_name"] = branch_name
            client = ClientManipulator.get_client(user_id, element["client"])
            if client.get("data"):
                client_tax_number = client["data"][0]["tax_number"]
                client_name = client["data"][0]["client_name"]
                result["data"][result["data"].index(element)]["client"] = client_name
                result["data"][result["data"].index(element)]["client_tax_number"] = client_tax_number
        return {"status":result["status"], "data":result["data"], "number_of_records": len(result["data"])}


    @classmethod
    def get_all_invoices_or_reports_or_types(cls, table_name,user_id):
        result = DBManipulator.select_query(table_name, {"user_id":user_id})
        for invoice_count in range(len(result["data"])):
            invoice_data = cls.get_specific_invoice(result["data"][invoice_count]["invoice_code"], user_id)
            if invoice_data.get("status") == False:
                result["data"][invoice_count]["invoice"] = result["data"][invoice_count]["invoice_code"]
            else:
                result["data"][invoice_count]["invoice"] = invoice_data["data"]
        return {"status":result["status"], "data":result["data"], "number_of_records": len(result["data"])}

    @classmethod
    def delete_sent_invoice(cls,invoice_code, user_id):
        result = DBManipulator.select_query("invoice", {"$and":[{"invoice_code":invoice_code, "user_id":user_id}]})
        if result.get("data"):
            result["data"][0]["total_invoice"] = 0
            update_result = cls.edit("invoice", result, {"invoice_code":invoice_code})
            update_result = update_result["data"]
            return {"status":update_result["status"], "data":{"invoice_code":update_result["data"][0]["invoice_code"], "sent_lable":update_result["data"][0]["sent_lable"]}}
        else:
            return {"status":False, "data":f"No invoice with this invoice code {invoice_code}, and with this user id {user_id}"}
    # TODO refactor the code to support code principals
    @classmethod
    def send_invoices_integration(cls, invoices_code, user_id):
        bad_result = []
        result  = cls.gather_invoices_data_for_integration(invoices_code, user_id)
        if result.get("data"):
            for i in  result["data"]["invoice_lines"]:
                del i["type_group"]
        try:
            #TODO send needed data to the integration
            r = httpx.post(f'{config("MIDDEL_WARE_HOST")}:{config("MIDDEL_WARE_PORT")}{config("MIDDEL_WARE_ENDPOINT")}', data= result)
            for invoice_code in invoices_code:
                result_invoice = DBManipulator.select_query("invoice", {"$and":[{"invoice_code":invoice_code, "user_id":user_id}]})
                if result.get("data"):
                    result_invoice["data"][0]["sent_lable"] = True
                    result_invoice["data"][0]["invoice_send_time"] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                    if r.json()["uuid"]:
                        result_invoice["data"][0]["invoice_uuid"] = r.json()["uuid"]
                    if r.json()["url"]:
                        result_invoice["data"][0]["invoice_url"] = r.json()["url"]

                    update_result = cls.edit("invoice", result_invoice["data"][0], {"invoice_code":invoice_code})
                    update_result = update_result["data"]
                else:
                    bad_result.append(result["data"][0]["invoice_code"])
            return {"status":True, "data":update_result}
        except Exception as ex:
            bad_result.append(result["data"][0]["invoice_code"])
    @classmethod
    def gather_invoices_data_for_integration(cls,invoices_code, user_id):
        bad_result = []
        document_types = {"invoice":"I", "add":"d", "discount":"c"}
        sub_tax_type = {"T1":"v009", "T2":"tbl02", "T3":"tbl01", "T4":"w002"}

        obj_for_integration = {"issure_data":{"address":{}},"reciver_data":{"address":{}}, "payment":{}, "delivery":{}, "invoice_lines":[], "taxTotals":[], "login_data":{}}
        for invoice_code in invoices_code:
            result = DBManipulator.select_query("invoice", {"$and":[{"invoice_code":invoice_code, "user_id":user_id}]})
            if result.get("data"):
                result["data"][0]["sent_lable"] = True
                try:
                    result_data = cls.get_info_invoice(invoice_code, user_id)
                    user_data = User.get_user(user_id)
                    data = result_data["data"][0]
                    # issure data
                    if data.get("branch"):
                        obj_for_integration["issure_data"]["address"]["branchID"] = data["branch"][0]["account_branch_code"]
                        obj_for_integration["issure_data"]["address"]["street"] = data["branch"][0]["brnach_name_ar"]
                        obj_for_integration["issure_data"]["address"]["regionCity"] = data["branch"][0]["brnach_name_ar"]
                        obj_for_integration["issure_data"]["address"]["buildingNumber"] = data["branch"][0]["brnach_name_ar"]
                        obj_for_integration["issure_data"]["address"]["postalCode"] = data["branch"][0]["brnach_name_ar"]

                        obj_for_integration["issure_data"]["address"]["floor"] = "1"
                        obj_for_integration["issure_data"]["address"]["room"] = ""
                        obj_for_integration["issure_data"]["address"]["landmark"] =""
                        obj_for_integration["issure_data"]["address"]["additionalInformation"] = ""
                        obj_for_integration["issure_data"]["address"]["governate"] = "Egypt"
                        obj_for_integration["issure_data"]["address"]["country"] = "EG"
                    if user_data.get("data"):
                        obj_for_integration["issure_data"]["branchID"] = data["branch"][0]["account_branch_code"]
                        obj_for_integration["issure_data"]["id"] = user_data["data"][0]["tax_number"]
                        obj_for_integration["issure_data"]["name"] = user_data["data"][0]["name"]
                        obj_for_integration["taxpayerActivityCode"] = user_data["data"][0]["activity_code"]
                        obj_for_integration["login_data"]["client_id"] = user_data["data"][0]["client_id"]
                        obj_for_integration["login_data"]["client_secret_1"] = user_data["data"][0]["client_secret_1"]
                        obj_for_integration["login_data"]["client_secret_2"] = user_data["data"][0]["client_secret_2"]


                    # reciver data

                    if data.get("client"):
                        obj_for_integration["reciver_data"]["address"]["street"] = data["client"][0]["address"]
                        obj_for_integration["reciver_data"]["address"]["regionCity"] = data["client"][0]["address"]
                        obj_for_integration["reciver_data"]["address"]["buildingNumber"] = data["client"][0]["address"]
                        obj_for_integration["reciver_data"]["address"]["postalCode"] = data["client"][0]["address"]
                        obj_for_integration["reciver_data"]["address"]["floor"] = "1"
                        obj_for_integration["reciver_data"]["address"]["room"] = ""
                        obj_for_integration["reciver_data"]["address"]["landmark"] =""
                        obj_for_integration["reciver_data"]["address"]["additionalInformation"] = ""
                        obj_for_integration["reciver_data"]["id"] = data["client"][0]["tax_number"]
                        obj_for_integration["reciver_data"]["name"] = data["client"][0]["client_name"]
                        obj_for_integration["reciver_data"]["branchID"] = data["client"][0]["client_code_number"]
                        obj_for_integration["reciver_data"]["street"] = data["client"][0]["address"]

                    if data.get("countryCode"):
                        obj_for_integration["reciver_data"]["country"] = data["countryCode"]
                    if data.get("country"):
                        obj_for_integration["reciver_data"]["governate"] = data["country"]
                        obj_for_integration["reciver_data"]["address"]["governate"] = data["country"]
                    # invoice data
                    if data.get("invoice_type"):
                        obj_for_integration["documentType"] = document_types[data["invoice_type"]]
                    if data.get("invoice_code"):
                        obj_for_integration["internalID"] = data["invoice_counter"]
                    obj_for_integration["documentTypeVersion"] = "1.0"
                    obj_for_integration["dateTimeIssued"] = data["date"]
                    obj_for_integration["purchaseOrderReference"] = ""
                    obj_for_integration["purchaseOrderDescription"] = ""
                    obj_for_integration["salesOrderReference"] = ""
                    obj_for_integration["salesOrderDescription"] = ""
                    obj_for_integration["proformaInvoiceNumber"] = ""
                    obj_for_integration["proformaInvoiceNumber"] = ""
                    obj_for_integration["payment"]["bankName"] = ""
                    obj_for_integration["payment"]["bankAddress"] = ""
                    obj_for_integration["payment"]["bankAccountNo"] = ""
                    obj_for_integration["payment"]["bankAccountIBAN"] = ""
                    obj_for_integration["payment"]["swiftCode"] = ""
                    obj_for_integration["delivery"]["approach"] = "0"
                    obj_for_integration["delivery"]["packaging"] = "0"
                    obj_for_integration["delivery"]["dateValidity"] = data["date"]
                    obj_for_integration["delivery"]["exportPort"] = ""
                    obj_for_integration["delivery"]["grossWeight"] = 0.0
                    obj_for_integration["delivery"]["netWeight"] = 0.0
                    obj_for_integration["delivery"]["terms"] = ""
                    ## invoice lines
                    obj_for_integration["totalDiscountAmount"] = 0
                    obj_for_integration["totalSalesAmount"] = 0
                    obj_for_integration["netAmount"] = 0
                    obj_for_integration["taxTotals_1"] = 0
                    obj_for_integration["taxTotals_2"] = 0
                    obj_for_integration["totalAmount"] = 0
                    number_of_items = len(data["invoice_types"]["invoice_type"])
                    core_ratio = data["discount_ratio"] / number_of_items
                    core_value = data["discount_value"] / number_of_items
                    for element in data["invoice_types"]["invoice_type"]:
                        invoice_lines = {}
                        for key in element:
                            if isinstance(element[key], list):
                                for sub_key in element[key]:
                                    invoice_lines["description"] = sub_key['type_name']
                                    invoice_lines["itemType"] = sub_key['tax_code_type']
                                    invoice_lines["itemCode"] = sub_key['tax_code']
                                    invoice_lines["unitType"] = sub_key['unit_of_measurment']
                                    invoice_lines["internalCode"] = sub_key['account_type_code']
                                    invoice_lines["type_group"] = sub_key['type_group'][0]["group_name_ar"]
                                    tax_type = sub_key['tax_type']
                                    tax_percentage = sub_key['tax_percentage']
                                    amountEGP = sub_key['price']
                                invoice_lines["unitValue"] = {"currencySold":"EGP","amountEGP":sub_key['price']}
                                invoice_lines["discount"] = {"rate":element['type_comm_ratio'],"amount": "" }
                                invoice_lines["salesTotal"] = (int(element["amount"]) * int(amountEGP))
                                invoice_lines["discount"]["amount"] = int(invoice_lines["salesTotal"]) - int(element['total_money_type'])
                                invoice_lines["quantity"] = element["amount"]
                                invoice_lines["netTotal"] = int(invoice_lines["salesTotal"]) - int(invoice_lines["discount"]["amount"])
                                invoice_lines["taxableItems"] = [{"taxType": tax_type, "amount": element["type_added_tax"], "subType": sub_tax_type[tax_type], "rate": tax_percentage},
                                                                {"taxType": "T4", "amount": core_value, "subType": "W002", "rate": core_ratio}]
                                invoice_lines["total"] = int(invoice_lines["salesTotal"]) +int(element["type_added_tax"]) + int(invoice_lines["taxableItems"][1]["amount"])- int(invoice_lines["discount"]["amount"])
                                obj_for_integration["totalDiscountAmount"] += invoice_lines["discount"]["amount"]
                                obj_for_integration["totalSalesAmount"] += invoice_lines["salesTotal"]
                                obj_for_integration["netAmount"] += invoice_lines["netTotal"]
                                obj_for_integration["taxTotals_1"] += invoice_lines["taxableItems"][0]["amount"]
                                obj_for_integration["taxTotals_2"] += invoice_lines["taxableItems"][1]["amount"]
                                obj_for_integration["totalAmount"] += invoice_lines["total"]

                        obj_for_integration["invoice_lines"].append(invoice_lines)
                        obj_for_integration["taxTotals"]=[
                        {
                            "taxType": invoice_lines["taxableItems"][0]["taxType"],
                            "amount": obj_for_integration["taxTotals_1"]
                        },
                        {
                            "taxType": "T4",
                            "amount": obj_for_integration["taxTotals_2"]
                        }
                        ]
                        del obj_for_integration["taxTotals_1"]
                        del obj_for_integration["taxTotals_2"]

                        return {"status":True, "data":obj_for_integration}
                except Exception as ex:
                    bad_result.append(result["data"][0]["invoice_code"])

            else:
                return {"status":False}
    @classmethod
    def get_invoices_integration(cls, user_id):
        result = DBManipulator.select_query("invoice", {"user_id":user_id})
        new_data = []
        for element in result["data"]:
            if element["sent_lable"] == False:
                branch = BranchManipulator.get_branch(element["branch"], user_id)
                if branch.get("data"):
                    branch_name = branch["data"][0]["brnach_name_ar"]
                    result["data"][result["data"].index(element)]["branch_name"] = branch_name
                client = ClientManipulator.get_client(user_id, element["client"])
                if client.get("data"):
                    client_tax_number = client["data"][0]["tax_number"]
                    client_name = client["data"][0]["client_name"]
                    result["data"][result["data"].index(element)]["client"] = client_name
                    result["data"][result["data"].index(element)]["client_tax_number"] = client_tax_number
                new_data.append(result["data"][result["data"].index(element)])
        return {"status":result["status"], "data":new_data, "number_of_records": len(new_data)}

    @classmethod
    def get_specific_invoice(cls, invoice_code, user_id):
        invoice_types = []
        result = DBManipulator.select_query("invoice", {"$and":[{"invoice_code":invoice_code, "user_id":user_id}]})
        if result.get("data"):
            result["data"][0]["client"] = ClientManipulator.get_client(user_id, result["data"][0]["client"])["data"]
            result["data"][0]["branch"] = BranchManipulator.get_branch(result["data"][0]["branch"],user_id)["data"]
            invoice_types_codes = result["data"][0]["invoice_types"]
            for invoice_type_code in invoice_types_codes:
                invoice_types.append(cls.get_specific_invoices_types([invoice_type_code],user_id)["data"])
            if result["status"] == True:
                result["data"][0]["invoice_types"] = {"invoice_type":invoice_types}
        else:
            result["status"] = False
            result["data"] = {
                "errors":{
                    "status":False,
                    "title":"No invoice  found",
                    "msg":f"No type added with this  Invoice {invoice_code}"
                }
            }

        return {"status":result["status"], "data":result["data"]}

    @classmethod
    def get_invoice_reports_related_to_invoce(cls, invoice_id, user_id):
        result = DBManipulator.select_query("invoice_report", {"$and":[{"invoice_code":invoice_id, "user_id":user_id}]})
        return {"status":result["status"], "data":result["data"]}

    @classmethod
    def get_info_invoice(cls, invoice_code, user_id):
        invoice_data = DBManipulator.select_query("invoice", {"$and":[{"invoice_code":invoice_code, "user_id":user_id}]})
        if invoice_data.get("data"):
            invoice_data["data"][0]["client"] = ClientManipulator.get_client(user_id, invoice_data["data"][0]["client"])["data"]
            invoice_data["data"][0]["branch"] = BranchManipulator.get_branch(invoice_data["data"][0]["branch"],user_id)["data"]
            invoice_types_codes = invoice_data["data"][0]["invoice_types"]
            invoice_types = cls.get_specific_invoices_types(invoice_types_codes,user_id)["data"]
            invoice_reports = cls.get_invoice_reports_related_to_invoce(invoice_code, user_id)["data"]
            if invoice_data["status"] == True:
                invoice_data["data"][0]["invoice_types"] = {"invoice_type":invoice_types}
                invoice_data["data"].append({"invoice_reports":invoice_reports})
        else:
            invoice_data["status"] = False
            invoice_data["data"] = {
                "errors":{
                    "status":False,
                    "title":"No invoice  found",
                    "msg":f"No type added with this  Invoice {invoice_code}"
                }
            }
        return {"status":invoice_data["status"], "data":invoice_data["data"]}

    @classmethod
    def get_specific_invoice_report(cls, report_code, user_id):
        result = DBManipulator.select_query("invoice_report", {"$and":[{"report_code":report_code, "user_id":user_id}]})
        return {"status":result["status"], "data":result["data"]}

    @classmethod
    def select_by_date(cls, table_name, start_date , end_date, user_id):
        dates_in_between = Helper.get_dates_in_between(end_date, start_date)
        invoices = []
        for date in dates_in_between:
            result = DBManipulator.select_query(table_name, {"$and":[{"date":date, "user_id":user_id}]})["data"]
            print(f"{date} ====> {user_id} ==> {result}")
            invoices.append(result)
        return {"status":True, "data":invoices}

    @classmethod
    def edit(cls, table_name, data, unique_value):
        if data.get("unique_value"):
            del data["unique_value"]
        result = DBManipulator.update_row(table_name, [data], unique_value)
        return {"status":result["status"], "data":result["data"]}

    @classmethod
    def delete_row(cls, table_name,key, value):
        result =DBManipulator.delete_row(table_name,key,value)
        return {"status" : result["status"], "data":result["data"]}

    @classmethod
    def export_invoices_reports(cls, data):
        document_types = {"I":"فاتورة", "d":"اشعار دائن", "c":"اشعار مدين"}

        if data["start_date"] and data["end_date"]:
            temp_array = []
            result = cls.select_by_date("invoice",data["start_date"], data["end_date"], data["user_id"])
            if result.get("data"):
                for i in range(len(result["data"])):
                    for element in result["data"][i]:
                        temp_array.append(element)
                result["data"] = temp_array
        else:
            result = cls.get_all_invoices_or_reports_or_types("invoice",data["user_id"])
        data_spacific_list = []
        invoices = []
        try:
            f = open("utilities/conf/app_info.json")
            json_data = json.load(f)
            if result.get("data"):
                directory_path = os.path.join(data["file_path"],data["user_id"])
                zipObj = ZipFile(f'{directory_path}.zip', 'w')

                for element in result["data"]:
                    invoices.append(element["invoice_code"])

                result_data = cls.gather_invoices_data_for_integration(["6029fc9c6f6248a69204725f4db8538f"],data["user_id"])
                user_data = User.get_user(data["user_id"])
                info_detail_dict = {}
                data = result_data["data"]

                # invoice data
                info_detail_dict["رقم المستند"] = data["internalID"]
                info_detail_dict["نوع المستند"] = document_types[data["documentType"]]
                info_detail_dict["تاريخ الإصدار"] = data["dateTimeIssued"]
                info_detail_dict["تاريخ الارسال"] = data["dateTimeIssued"]
                for element in data["invoice_lines"]:
                    info_detail_dict["الخصم التجارى"] = element["discount"]["amount"]
                    info_detail_dict["مجموعة الصنف "] = element["discount"]["amount"]

                    info_detail_dict["الكود الضريبي"] = element["itemCode"]
                    if element["itemType"] == "EGS":
                        info_detail_dict["كود الصنف"] = element["itemCode"].split("-")[2]
                    else:
                        info_detail_dict["كود الصنف"] = element["itemCode"]
                    info_detail_dict["اسم الصنف"] = element["description"]
                    info_detail_dict["كمية"] = element["quantity"]
                    info_detail_dict["الوحدة"] = element["unitType"]
                    info_detail_dict["سعر الوحدة"] = element["unitValue"]["amountEGP"]

                    info_detail_dict["اجمالى الفاتورة قبل الخصم"] = element["salesTotal"]
                    info_detail_dict["صافى القيمة"] = element["netTotal"]
                    info_detail_dict["ضريبة القيمه المضافه"] = element["taxableItems"][0]["amount"]
                    info_detail_dict["ضريبة المنبع"] = element["taxableItems"][1]["amount"]
                    info_detail_dict["صافى المستحق"] = element["total"]
                    # issure data
                    if user_data.get("data"):
                        info_detail_dict["رقم التسجيل الضريبي"] = user_data["data"][0]["tax_number"]
                        info_detail_dict["اسم الشركة"] = user_data["data"][0]["name"]
                    if data.get("issure_data"):
                        info_detail_dict["الفرع"] = data["issure_data"]["address"]["street"]
                        info_detail_dict["رقم التسجيل الضريبي"] = data["issure_data"]["id"]
                        info_detail_dict["اسم الشركة"] = data["issure_data"]["name"]

                    # reciver data
                    if data.get("reciver_data"):
                        info_detail_dict["كود العميل"] = data["reciver_data"]["id"]
                        info_detail_dict["العميل"] = data["reciver_data"]["name"]
                        info_detail_dict["الدوله"] = data["reciver_data"]["governate"]
                        info_detail_dict["الفرع"] = data["reciver_data"]["street"]
                    info_detail_dict["الرقم التعريفى"] = ""
                    info_detail_dict["حالة الفاتورة "] = "ارسلت"
                    data_spacific_list.append(info_detail_dict)

                spacific_df = pd.DataFrame(data_spacific_list)
                spacific_df.to_excel(f'{directory_path}-spacific.xlsx' , index=False)
                zipObj.write(f'{directory_path}-spacific.xlsx')
                os.remove(f'{directory_path}-spacific.xlsx')
                file_path_zip = directory_path+".zip"
                file_path_zip = file_path_zip.replace("/", "+")
                file_path_zip = file_path_zip[1:]
                datetime_object = str(datetime.datetime.now()).replace(" ", "")

                return {"status":result["status"], "data":{"file_paht":f'{json_data["application_data"]["APPLICATION_IP"]}:{json_data["application_data"]["APPLICATION_PORT"]}/api/download/{file_path_zip}'}}
            else:
                return {"status":"False", "data":""}
        except Exception as ex:
            return {"status":"False", "error": str(ex)}




        #             # invoice_types = cls.get_specific_invoices_types(element["invoice_types"],data["user_id"])["data"]
        #             # branch = BranchManipulator.get_branch(element["branch"], data["user_id"])
        #             # if branch.get("data"):
        #             #     branch_name = branch["data"][0]["brnach_name_ar"]
        #             # client = ClientManipulator.get_client(data["user_id"], element["client"])
        #             # if client.get("data"):
        #             #     client_tax_number = client["data"][0]["tax_number"]
        #             #     client_name = client["data"][0]["client_name"]

        #         #     if invoice_types:
        #         #         for i in invoice_types:

        #         #             info_detail_dict["رقم المستند"] = element["invoice_counter"]
        #         #             info_detail_dict["invoice_date"] = element["date"]
        #         #             info_detail_dict["invoice_client_name"] = client_name
        #         #             info_detail_dict[" invoice_client_tax_number"] = client_tax_number
        #         #             info_detail_dict["type_name"] = i["invoice_type_id"][0]["type_name"]
        #         #             tax_code = StaticTables.get_table_with_id("tax_types",i["invoice_type_id"][0]["tax_type"])
        #         #             if tax_code.get("data"):
        #         #                 info_detail_dict["tax_code"] = i["invoice_type_id"][0]["tax_type"]
        #         #                 info_detail_dict["tax_name_ar"] = tax_code["data"][0]["Desc_ar"]
        #         #                 info_detail_dict["tax_name_en"] = tax_code["data"][0]["Desc_en"]
        #         #             unit_of_mesurment = StaticTables.get_table_with_id("measurement_units",i["invoice_type_id"][0]["unit_of_measurment"])
        #         #             if unit_of_mesurment.get("data"):
        #         #                 info_detail_dict["unit_code"] = i["invoice_type_id"][0]["unit_of_measurment"]
        #         #                 info_detail_dict["unit_name_ar"] = unit_of_mesurment["data"][0]["desc_ar"]
        #         #                 info_detail_dict["unit_name_en"] = unit_of_mesurment["data"][0]["desc_en"]

        #         #             info_detail_dict["group_name_ar"] = i["invoice_type_id"][0]["type_group"][0]["group_name_ar"]
        #         #             info_detail_dict["group_name_en"] = i["invoice_type_id"][0]["type_group"][0]["group_name_en"]

        #         #             info_detail_dict["tax_type"] = i["invoice_type_id"][0]["tax_type"]
        #         #             info_detail_dict["tax_percentage"] = i["invoice_type_id"][0]["tax_percentage"]
        #         #             info_detail_dict["total_money_of_type"] = i["total_money_type"]
        #         #             info_detail_dict["amount"] = i["amount"]
        #         #             data_spacific_list.append(info_detail_dict)
        #         #         spacific_df = pd.DataFrame(data_spacific_list)
        #         #         spacific_df.to_excel(f'{directory_path}-spacific.xlsx' , index=False)
        #         #         zipObj.write(f'{directory_path}-spacific.xlsx')
        #         #         os.remove(f'{directory_path}-spacific.xlsx')

        #         #     info_general_dict["invoice_num"] = element.get("invoice_counter", "")
        #         #     info_general_dict["invoice_date"] = element.get("date","")
        #         #     info_general_dict["invoice_type"] = element.get("invoice_type","")
        #         #     info_general_dict["payment_type"] = element.get("payment_type","")
        #         #     info_general_dict["notes"] = element.get("notes","")
        #         #     info_general_dict["discount_value"] = element.get("discount_value","")
        #         #     info_general_dict["total_added_tax"] = element.get("total_added_tax","")
        #         #     info_general_dict["total_comm_tax"] = element.get("total_comm_tax","")
        #         #     info_general_dict["country"] = element.get("country","")
        #         #     info_general_dict["total_after_comm_tax"] = element.get("total_after_comm_tax", "")
        #         #     info_general_dict["deduction_value"] = element.get("deduction_value", "")
        #         #     info_general_dict["type_comm_ratio"] = element.get("type_comm_ratio", "")
        #         #     info_general_dict["total_before_taxes"] = element.get("total_before_taxes", "")
        #         #     info_general_dict["sent_lable"] = element.get("sent_lable", "")

        #         #     info_general_dict["invoice_client_name"] = client_name
        #         #     info_general_dict[" invoice_client_tax_number"] = client_tax_number
        #         #     info_general_dict["invoice_branch"] = branch_name
        #         #     info_general_dict["invoice_discount"] = element.get("discount_ratio", "")
        #         #     info_general_dict["invoice_total"] = element.get("total_invoice","")
        #         #     data_list.append(info_general_dict)
        #         # general_df = pd.DataFrame(data_list)
        #         # general_df.to_excel(f'{directory_path}-general.xlsx' , index=False)
        #         # zipObj.write(f'{directory_path}-general.xlsx')
        #         # os.remove(f'{directory_path}-general.xlsx')
        #         # file_path_zip = directory_path+".zip"
        #         # file_path_zip = file_path_zip.replace("/", "+")
        #         # file_path_zip = file_path_zip[1:]
        #         # datetime_object = str(datetime.datetime.now()).replace(" ", "")
        #         # return {"status":result["status"], "data":{"file_paht":f'{json_data["application_data"]["APPLICATION_IP"]}:{json_data["application_data"]["APPLICATION_PORT"]}/api/download/{file_path_zip}'}}
        #     else:
        #         return {"status":"False", "data":""}
        # except Exception as ex:
        #     return {"status":"False", "error": str(ex)}

# invoice types data
# data = {
#     "amount":6,
#     "total_money_type":5000,
#     "invoice_type_id":12222,
#     "invoice_id":13,
#     "user_id": "sdsdf1231asdasd",
#     "report_id":NULL
# }
# # invoice report data

# data1 = {
#     "date":"2022-11-02",
#     "report_type":"discount",
#     "invoice_id":5,
#     "notes":"hello",
#     "invoice_types":[12,33,44,2],
#     # get_specific_invoices_types
#     "user_id":1,
# }
# # # invoice data

# data2 = {
#     "date":"2022-11-02",
#     "client":12,
#     "payment_type":"cash",
#     "discount_ratio":1/10,
#     "total_invoice":2000,
#     "notes":"helllo",
#     "invoice_types":[12,33,44,2],
#     "user_id":1,
# }

# DBManipulator({"host":"155.133.22.3","port":27017})
# db = DBManipulator.create_session("accountant_db")
# print(Insend_invoices_integration(["2fff3d5dcb7d48f18f39dbfb08192831", "8fe8dc9d57e04b4784b7698d469a47e1", "dd01eca1e78a4ddd9febb89ff6176e3b"], "c2a0c6abc57140be87f6d7a9ae187db9"))
# print(InvoiceManipulator.get_specific_invoice_report("f6a6c11fa7db41f99dc45b92c8c49834",5,1))

# # print(InvoiceManipulator.get_specific_invoices_types("0dae5287fdfb411fb8ff5ca6db331f43","sdsdf1231asdasd"))
# # print(InvoiceManipulator.get_all_invoices_types(13, "sdsdf1231asdasd"))
# print(InvoiceManipulator.create_invoice_or_report_or_type("invoice_report","report_code", data2))
# print(InvoiceManipulator.select_by_date("2022-11-02", "2022-11-02", "170474f5030c487c93f59296d99b4def" )[0][1])

