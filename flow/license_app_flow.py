from db import DBManipulator
from src import LicenseFlow
from utilities.logger_settings import LoggerSettings

class LicenseAppFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def license_option(cls, data, action, request_id):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to license option')
        if action == "create":
            logger.debug(f'[{request_id}] request recived to license option with action = {action}')
            result = LicenseFlow.license_handeler("create",data)
            logger.debug(f'[{request_id}] request done on license option with action = {action}')
        # elif action == "edite":
        #     result = LicenseFlow.license_handeler("update",data,data["unique_value"][""])
        elif action == "delete":
            logger.debug(f'[{request_id}] request recived to license option with action = {action}')
            result = LicenseFlow.license_handeler("delete",data)
            logger.debug(f'[{request_id}] request done on license option with action = {action}')
        elif action == "get_all_licenses":
            logger.debug(f'[{request_id}] request recived to license option with action = {action}')
            result = LicenseFlow.license_handeler("select_all",data)
            logger.debug(f'[{request_id}] request done on license option with action = {action}')
        elif action == "get_license":
            logger.debug(f'[{request_id}] request recived to license option with action = {action}')
            result = LicenseFlow.license_handeler("select",data)
            logger.debug(f'[{request_id}] request done on license option with action = {action}')
        else:
            result = f"You should specify right action but what we recive is {action}"

        return result