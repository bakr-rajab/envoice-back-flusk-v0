import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/invoice_module")
from ..flow.invoice_flow import InvoiceFlow

class InvoiceCore:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_invoice(cls, data):
        return InvoiceFlow.invoice_handeler("create", data)

    @classmethod
    def edite_invoice(cls, data):
        return InvoiceFlow.invoice_handeler("update",data, data["invoice_code"])

    @classmethod
    def get_invoice(cls, data):
        return InvoiceFlow.invoice_handeler("select", data)

    @classmethod
    def get_all_invoice(cls, data):
        return InvoiceFlow.invoice_handeler("select_all", data)

    @classmethod
    def delete_invoice(cls, data):
        return InvoiceFlow.invoice_handeler("delete", data["key"], data["value"])

    @classmethod
    def delete_sent_invoice(cls, data):
        return InvoiceFlow.invoice_handeler("delete_sent", data)

    @classmethod
    def export_invoice_reports(cls, data):
        return InvoiceFlow.invoice_handeler("export_invoice_report",data)