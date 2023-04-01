from db import DBManipulator
from src import UserFlow
from utilities.logger_settings import LoggerSettings

class UserAppFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def user_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to user option')

        number_of_records = 0
        if action == "create":
            logger.debug(f'[{request_id}] request recived to user option with action = {action}')
            result = UserFlow.user_handeler("create",data)
            logger.debug(f'[{request_id}] request done on user option with action = {action}')

        elif action == "edit":
            logger.debug(f'[{request_id}] request recived to user option with action = {action}')
            result = UserFlow.user_handeler("update",data,data["unique_value"]["tax_number"])
            logger.debug(f'[{request_id}] request done on user option with action = {action}')

        elif action == "delete":
            logger.debug(f'[{request_id}] request recived to user option with action = {action}')
            result = UserFlow.user_handeler("delete",data)
            logger.debug(f'[{request_id}] request done on user option with action = {action}')

        elif action == "get_all_users":
            logger.debug(f'[{request_id}] request recived to user option with action = {action}')
            result = UserFlow.user_handeler("select_all",data)
            logger.debug(f'[{request_id}] request done on user option with action = {action}')

        elif action == "get_user":
            logger.debug(f'[{request_id}] request recived to user option with action = {action}')
            result = UserFlow.user_handeler("select",data)
            logger.debug(f'[{request_id}] request done on user option with action = {action}')

        elif action == "auth":
            logger.debug(f'[{request_id}] request recived to user option with action = {action}')
            result = UserFlow.user_handeler("auth",data)
            logger.debug(f'[{request_id}] request done on user option with action = {action}')

        else:
            logger.debug(f'[{request_id}] request recived to user option with no action')
            result = f"You should specify right action but what we recive is {action}"

        return result