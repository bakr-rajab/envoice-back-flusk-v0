import sys
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/invoice_module/")

from ..invoice_maipulator import InvoiceManipulator


class InvoiceTypeFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def invoice_type_handeler(cls,task_name, data= "", unique_value= "" ):

        if task_name == "create":
            status= InvoiceManipulator.create_invoice_or_report_or_type("invoice_type", "invoice_type_code", data)
        elif task_name == "update":
            status = InvoiceManipulator.edit("invoice_type",data,{"invoice_code":unique_value})
        elif task_name == "delete":
            status = InvoiceManipulator.delete_row("invoice_type",data["key"], data["value"])
        elif task_name == "select":
            status = InvoiceManipulator.get_specific_invoices_types(data["invoice_type_code"], data["user_id"])
        elif task_name == "select_all":
            status = InvoiceManipulator.get_all_invoices_or_reports_or_types("invoice_type",data["user_id"])
        elif task_name == "filter":
            status = InvoiceManipulator.select_by_date("invoice_type",data["start_date"], data["end_date"], data["user_id"])
        elif task_name == "import":
            status = InvoiceManipulator.create_invoice_types_with_import(data)
        else:
            status_code = 500
            msg =  f"Couldn't create Traning file for the following reason: " \
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