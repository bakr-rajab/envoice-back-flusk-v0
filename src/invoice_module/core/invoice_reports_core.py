import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/invoice_module")
from ..flow.invoice_reports_flow import InvoiceReportFlow

class InvoiceReportCore:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_invoice_report(cls, data):
        return InvoiceReportFlow.invoice_report_handeler("create", data)

    @classmethod
    def edite_invoice_report(cls, data):
        return InvoiceReportFlow.invoice_report_handeler("update",data, data["report_code"])

    @classmethod
    def get_invoice_report(cls, data):
        return InvoiceReportFlow.invoice_report_handeler("select", data)

    @classmethod
    def get_all_invoice_report(cls, data):
        return InvoiceReportFlow.invoice_report_handeler("select_all", data)

    @classmethod
    def delete_invoice_report(cls, data):
        return InvoiceReportFlow.invoice_report_handeler("delete", data["key"], data["value"])