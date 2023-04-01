from flow import BranchAppFlow, ClientAppFlow, InvoiceAppFlow, StaticAppFlow, TypeAppFlow, UserAppFlow, static_app_flow, LicenseAppFlow, PlanAppFlow
from utilities.logger_settings import LoggerSettings

class InboundUtility:

    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def request_handeler(cls, target, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()

        if target == "user" :
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = UserAppFlow.user_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "client" :
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = ClientAppFlow.client_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "branch":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = BranchAppFlow.branch_option(data, action,request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')


        elif target == "static":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = StaticAppFlow.static_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "type":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = TypeAppFlow.type_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "type_group":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = TypeAppFlow.type_group_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "invoice":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = InvoiceAppFlow.invoice_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "invoice_type":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result= InvoiceAppFlow.invoice_type_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "invoice_report":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = InvoiceAppFlow.invoice_report_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "invoice_full_info":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = InvoiceAppFlow.invoice_report_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "license":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = LicenseAppFlow.license_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        elif target == "plan":
            logger.debug(f'[{request_id}] request recived with target =  {target}')
            data_result = PlanAppFlow.plan_option(data, action, request_id)
            logger.debug(f'[{request_id}] The output is  =  {data_result}, and the number of records = {data_result.get("number_of_records", 0)}')

        return data_result
