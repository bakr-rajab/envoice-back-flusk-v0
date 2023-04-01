from db import DBManipulator
from src import InvoiceFlow, InvoiceTypeFlow, InvoiceReportFlow
from utilities.logger_settings import LoggerSettings

class InvoiceAppFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def invoice_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to invoice option')

        if action== "create":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("create", data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "edite":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("update", data, data["unique_value"]["invoice_code"])
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "delete":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("delete",data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "delete_sent":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("delete_sent",data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "get_all_invoices":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("select_all",data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "get_invoice":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("select",data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "get_integration_invoices":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("get_integration_invoices",data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "send_invoices":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("send_invoices",data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "invoice_full_info":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("invoice_full_info",data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "export_invoice_report":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("export_invoice_report",data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        elif action== "import":
            logger.debug(f'[{request_id}] request recived to invoice option with action = {action}')
            result = InvoiceFlow.invoice_handeler("import",data)
            logger.debug(f'[{request_id}] request done on invoice option with action = {action}')
        else:
            result = f"You should specify right action but what we recive is {action}"

        return result

    @classmethod
    def invoice_type_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to invoice type option')

        if action== "create":
            logger.debug(f'[{request_id}] request recived to invoice type option with action = {action}')
            result = InvoiceTypeFlow.invoice_type_handeler("create",data)
            logger.debug(f'[{request_id}] request done on invoice type option with action = {action}')
        elif action== "edite":
            logger.debug(f'[{request_id}] request recived to invoice type option with action = {action}')
            result = InvoiceTypeFlow.invoice_type_handeler("update",data,data["unique_value"]["report_code"])
            logger.debug(f'[{request_id}] request done on invoice type option with action = {action}')
        elif action== "delete":
            logger.debug(f'[{request_id}] request recived to invoice type option with action = {action}')
            result = InvoiceTypeFlow.invoice_type_handeler("delete",data)
            logger.debug(f'[{request_id}] request done on invoice type option with action = {action}')
        elif action== "get_all_invoices_type":
            logger.debug(f'[{request_id}] request recived to invoice type option with action = {action}')
            result = InvoiceTypeFlow.invoice_type_handeler("select_all",data)
            logger.debug(f'[{request_id}] request done on invoice type option with action = {action}')
        elif action== "get_invoice_type":
            logger.debug(f'[{request_id}] request recived to invoice type option with action = {action}')
            result = InvoiceTypeFlow.invoice_type_handeler("select",data)
            logger.debug(f'[{request_id}] request done on invoice type option with action = {action}')
        elif action== "import":
            logger.debug(f'[{request_id}] request recived to invoice type option with action = {action}')
            result = InvoiceTypeFlow.invoice_type_handeler("import",data)
            logger.debug(f'[{request_id}] request done on invoice type option with action = {action}')
        else:
            result = f"You should specify right action but what we recive is {action}"

        return result

    @classmethod
    def invoice_report_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to invoice report option')

        if action== "create":
            logger.debug(f'[{request_id}] request recived to invoice report option with action = {action}')
            result = InvoiceReportFlow.invoice_report_handeler("create",data)
            logger.debug(f'[{request_id}] request done on invoice report option with action = {action}')
        elif action== "edite":
            logger.debug(f'[{request_id}] request recived to invoice report option with action = {action}')
            result = InvoiceReportFlow.invoice_report_handeler("update",data,data["unique_value"]["report_code"])
            logger.debug(f'[{request_id}] request done on invoice report option with action = {action}')
        elif action== "delete":
            logger.debug(f'[{request_id}] request recived to invoice report option with action = {action}')
            result = InvoiceReportFlow.invoice_report_handeler("delete",data)
            logger.debug(f'[{request_id}] request done on invoice report option with action = {action}')
        elif action== "get_all_invoices_report":
            logger.debug(f'[{request_id}] request recived to invoice report option with action = {action}')
            result = InvoiceReportFlow.invoice_report_handeler("select_all",data)
            logger.debug(f'[{request_id}] request done on invoice report option with action = {action}')
        elif action== "get_invoice_report":
            logger.debug(f'[{request_id}] request recived to invoice report option with action = {action}')
            result = InvoiceReportFlow.invoice_report_handeler("select",data)
            logger.debug(f'[{request_id}] request done on invoice report option with action = {action}')
        else:
            result = f"You should specify right action but what we recive is {action}"

        return result

