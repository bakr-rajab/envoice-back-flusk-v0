import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/invoice_module")
from ..flow.invoice_types_flow  import InvoiceTypeFlow

class InvoiceTypesCore:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_invoice_type(cls, data):
        return InvoiceTypeFlow.invoice_type_handeler("create", data)

    @classmethod
    def edite_invoice_type(cls, data):
        return InvoiceTypeFlow.invoice_type_handeler("update",data, data["invoice_type_code"])

    @classmethod
    def get_invoice_type(cls, data):
        return InvoiceTypeFlow.invoice_type_handeler("select", data)

    @classmethod
    def get_all_invoice_type(cls, data):
        return InvoiceTypeFlow.invoice_type_handeler("select_all", data)

    @classmethod
    def delete_invoice_type(cls, data):
        return InvoiceTypeFlow.invoice_type_handeler("delete", data["key"], data["value"])