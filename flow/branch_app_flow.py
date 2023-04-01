from db import DBManipulator
from src import BranchFlow
from utilities.logger_settings import LoggerSettings

class BranchAppFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def branch_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to branch option')
        if action == "create":
            logger.debug(f'[{request_id}] request recived to branch option with action = {action}')
            result = BranchFlow.branch_handeler("create", request_id, data)
            logger.debug(f'[{request_id}] request done on branch option with action = {action}')
        elif action == "edite":
            logger.debug(f'[{request_id}] request recived to branch option with action = {action}')
            result = BranchFlow.branch_handeler("update", request_id, data,data["unique_value"]["branch_code"])
            logger.debug(f'[{request_id}] request done on branch option with action = {action}')
        elif action == "delete":
            logger.debug(f'[{request_id}] request recived to branch option with action = {action}')
            result = BranchFlow.branch_handeler("delete",request_id, data)
            logger.debug(f'[{request_id}] request done on branch option with action = {action}')
        elif action == "get_all_branchs":
            logger.debug(f'[{request_id}] request recived to branch option with action = {action}')
            result = BranchFlow.branch_handeler("select_all",request_id, data)
            logger.debug(f'[{request_id}] request done on branch option with action = {action}')
        elif action == "get_branch":
            logger.debug(f'[{request_id}] request recived to branch option with action = {action}')
            result = BranchFlow.branch_handeler("select",request_id, data)
            logger.debug(f'[{request_id}] request done on branch option with action = {action}')
        elif action == "import":
            logger.debug(f'[{request_id}] request recived to branch option with action = {action}')
            result = BranchFlow.branch_handeler("import",request_id, data)
            logger.debug(f'[{request_id}] request done on branch option with action = {action}')
        else:
            result = f"You should specify right action but what we recive is {action}"

        return result