from db import DBManipulator
from src import PlansFlow
from utilities.logger_settings import LoggerSettings

class PlanAppFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def plan_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()

        logger.debug(f'[{request_id}] request recived to plan option')
        if action == "create":
            logger.debug(f'[{request_id}] request recived to plan option with action = {action}')
            result = PlansFlow.plan_handeler("create",data)
            logger.debug(f'[{request_id}] request done on plan option with action = {action}')
        elif action == "edit":
            logger.debug(f'[{request_id}] request recived to plan option with action = {action}')
            result = PlansFlow.plan_handeler("update",data,data["unique_value"]["plan_id"])
            logger.debug(f'[{request_id}] request done on plan option with action = {action}')
        elif action == "delete":
            logger.debug(f'[{request_id}] request recived to plan option with action = {action}')
            result = PlansFlow.plan_handeler("delete",data)
            logger.debug(f'[{request_id}] request done on plan option with action = {action}')
        elif action == "get_all_plans":
            logger.debug(f'[{request_id}] request recived to plan option with action = {action}')
            result = PlansFlow.plan_handeler("select_all",data)
            logger.debug(f'[{request_id}] request done on plan option with action = {action}')
        elif action == "get_plan":
            logger.debug(f'[{request_id}] request recived to plan option with action = {action}')
            result = PlansFlow.plan_handeler("select",data)
            logger.debug(f'[{request_id}] request done on plan option with action = {action}')
        else:
            result = f"You should specify right action but what we recive is {action}"

        return result