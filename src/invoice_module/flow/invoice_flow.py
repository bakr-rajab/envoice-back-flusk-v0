import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/invoice_module/")

from ..invoice_maipulator import InvoiceManipulator


class InvoiceFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def invoice_handeler(cls,task_name, data= "", unique_value= "" ):
        if task_name == "create":
            status= InvoiceManipulator.create_invoice_or_report_or_type("invoice","invoice_code",data)
        elif task_name == "update":
            status = InvoiceManipulator.edit("invoice",data, {"invoice_code":unique_value})
        elif task_name == "delete":
            status = InvoiceManipulator.delete_row("invoice",data["key"], data["value"])
        elif task_name == "select":
            status = InvoiceManipulator.get_specific_invoice(data["invoice_code"], data["user_id"])
        elif task_name == "send_invoices":
            status = InvoiceManipulator.send_invoices_integration(data["invoices_id"], data["user_id"])
        elif task_name == "get_integration_invoices":
            status = InvoiceManipulator.get_invoices_integration(data["user_id"])
        elif task_name == "select_all":
            status = InvoiceManipulator.get_all_invoices(data["user_id"])
        elif task_name == "filter":
            status = InvoiceManipulator.select_by_date("invoice",data["start_date"], data["end_date"], data["user_id"])
        elif task_name == "invoice_full_info":
            status = InvoiceManipulator.get_info_invoice(data["invoice_code"], data["user_id"])
        elif task_name == "export_invoice_report":
            status = InvoiceManipulator.export_invoices_reports(data)
        elif task_name == "import":
            status = InvoiceManipulator.create_invoice_with_import(data)
        else:
            status_code = 500
            msg =  f"Couldn't processed for following reason: " \
                    + f"the task name not valid should be one of those [create, update, delete, select] but we got {task_name}"
            return{
                "status_code":status_code,
                "title":"The task not found",
                "details": msg
            }
        if status == True:
                status_code = 200
                return status_code
        else:
                return status