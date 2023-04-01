from src import StaticDataFlow
from utilities.logger_settings import LoggerSettings

class StaticAppFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def static_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to static option')
        if action == "create":
            logger.debug(f'[{request_id}] request recived to static option with action = {action}')
            result = StaticDataFlow.static_data_handeler("create", data)
            logger.debug(f'[{request_id}] request done on static option with action = {action}')
            return result
        if action == "get_all_elements":
            logger.debug(f'[{request_id}] request recived to static option with action = {action}')
            result = StaticDataFlow.static_data_handeler("select_all",data)
            logger.debug(f'[{request_id}] request done on static option with action = {action}')
        elif action == "get_element":
            logger.debug(f'[{request_id}] request recived to static option with action = {action}')
            result = StaticDataFlow.static_data_handeler("select",data,data["code"])
            logger.debug(f'[{request_id}] request done on static option with action = {action}')
        elif action == "edite":
            logger.debug(f'[{request_id}] request recived to static option with action = {action}')
            result = StaticDataFlow.static_data_handeler("update",data,data["unique_value"]["code"])
            logger.debug(f'[{request_id}] request done on static option with action = {action}')
        elif action == "delete":
            logger.debug(f'[{request_id}] request recived to static option with action = {action}')
            result = StaticDataFlow.static_data_handeler("delete",data)
            logger.debug(f'[{request_id}] request done on static option with action = {action}')
        else:
            result = f"You should specify right action but what we recive is {action}"

        return result