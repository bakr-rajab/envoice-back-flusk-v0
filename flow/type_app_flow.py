from db import DBManipulator
from src import TypesFlow, TypesGroupsFlow
from utilities.logger_settings import LoggerSettings

class TypeAppFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def type_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to type option')
        if action == "create":
            logger.debug(f'[{request_id}] request recived to type option with action = {action}')
            result = TypesFlow.types_handeler("create",data)
            logger.debug(f'[{request_id}] request done on type option with action = {action}')

        elif action == "edit":
            logger.debug(f'[{request_id}] request recived to type option with action = {action}')
            result = TypesFlow.types_handeler("update",data,data["unique_value"]["type_code"])
            logger.debug(f'[{request_id}] request done on type option with action = {action}')

        elif action == "delete":
            logger.debug(f'[{request_id}] request recived to type option with action = {action}')
            result = TypesFlow.types_handeler("delete",data)
            logger.debug(f'[{request_id}] request done on type option with action = {action}')
        elif action == "get_all_types":
            logger.debug(f'[{request_id}] request recived to type option with action = {action}')
            result = TypesFlow.types_handeler("select_all",data)
            logger.debug(f'[{request_id}] request done on type option with action = {action}')
        elif action == "get_type":
            logger.debug(f'[{request_id}] request recived to type option with action = {action}')
            result = TypesFlow.types_handeler("select",data)
            logger.debug(f'[{request_id}] request done on type option with action = {action}')
        elif action == "import":
            logger.debug(f'[{request_id}] request recived to type option with action = {action}')
            result = TypesFlow.types_handeler("import",data)
            logger.debug(f'[{request_id}] request done on type option with action = {action}')
        else:
            result = {"status":False , "data":f"You should specify right action but what we recive is {action}"}

        return result

    @classmethod
    def type_group_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to type group option')
        if action == "create":
            logger.debug(f'[{request_id}] request recived to type group option with action = {action}')
            result = TypesGroupsFlow.types_groups_handeler("create",data)
            logger.debug(f'[{request_id}] request done on type group option with action = {action}')
        elif action == "edit":
            logger.debug(f'[{request_id}] request recived to type group option with action = {action}')
            result = TypesGroupsFlow.types_groups_handeler("update",data,data["unique_value"]["group_code"])
            logger.debug(f'[{request_id}] request done on type group option with action = {action}')
        elif action == "delete":
            logger.debug(f'[{request_id}] request recived to type group option with action = {action}')
            result = TypesGroupsFlow.types_groups_handeler("delete",data)
            logger.debug(f'[{request_id}] request done on type group option with action = {action}')
        elif action == "get_all_types_groups":
            logger.debug(f'[{request_id}] request recived to type group option with action = {action}')
            result = TypesGroupsFlow.types_groups_handeler("select_all",data)
            logger.debug(f'[{request_id}] request done on type group option with action = {action}')
        elif action == "get_type_group":
            logger.debug(f'[{request_id}] request recived to type group option with action = {action}')
            result = TypesGroupsFlow.types_groups_handeler("select",data)
            logger.debug(f'[{request_id}] request done on type group option with action = {action}')
        elif action == "import":
            logger.debug(f'[{request_id}] request recived to type group option with action = {action}')
            result = TypesGroupsFlow.types_groups_handeler("import",data)
            logger.debug(f'[{request_id}] request done on type group option with action = {action}')
        else:
            result = {"status":False , "data":f"You should specify right action but what we recive is {action}"}

        return result