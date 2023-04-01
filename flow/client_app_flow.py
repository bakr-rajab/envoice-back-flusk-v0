from db import DBManipulator
from src import ClientFlow
from utilities.logger_settings import LoggerSettings

class ClientAppFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def client_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        if action == "create":

            logger.debug(f'[{request_id}] request recived to client option with action = {action}')
            result = ClientFlow.client_handeler("create", request_id, data)
            logger.debug(f'[{request_id}] request done on client option with action = {action}')

        elif action == "edite":

            logger.debug(f'[{request_id}] request recived to client option with action = {action}')
            result = ClientFlow.client_handeler("update",request_id, data,data["unique_value"]["tax_number"])
            logger.debug(f'[{request_id}] request done on client option with action = {action}')

        elif action == "delete":
            logger.debug(f'[{request_id}] request recived to client option with action = {action}')
            result = ClientFlow.client_handeler("delete",request_id, data)
            logger.debug(f'[{request_id}] request done on client option with action = {action}')

        elif action == "get_all_clients":
            logger.debug(f'[{request_id}] request recived to client option with action = {action}')
            result = ClientFlow.client_handeler("select_all",request_id, data)
            logger.debug(f'[{request_id}] request done on client option with action = {action}')
        elif action == "get_client":
            logger.debug(f'[{request_id}] request recived to client option with action = {action}')
            result = ClientFlow.client_handeler("select",request_id, data)
            logger.debug(f'[{request_id}] request done on client option with action = {action}')
        elif action == "import":
            logger.debug(f'[{request_id}] request recived to client option with action = {action}')
            result = ClientFlow.client_handeler("import",request_id, data)
            logger.debug(f'[{request_id}] request done on client option with action = {action}')
        else:
            logger.debug(f'[{request_id}] request recived to client option with no action')
            result = f"You should specify right action but what we recive is {action}"

        return result