from ..client_manipulator import ClientManipulator
from utilities.logger_settings import LoggerSettings


class ClientFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def client_handeler(cls,task_name, request_id, data= "", unique_value= "" ):
        logger, _ = LoggerSettings.logger_setting()

        number_of_clients = 0
        if task_name == "create":
            logger.debug(f'[{request_id}] request recived to client option with task_name = {task_name}')
            status= ClientManipulator.create_client(data)
            logger.debug(f'[{request_id}] request done on client option with task_name = {task_name}')
        elif task_name == "update":
            logger.debug(f'[{request_id}] request recived to client option with task_name = {task_name}')
            status = ClientManipulator.edit_client(data,{"tax_number":unique_value})
            logger.debug(f'[{request_id}] request done on client option with task_name = {task_name}')
        elif task_name == "delete":
            logger.debug(f'[{request_id}] request recived to client option with task_name = {task_name}')
            status = ClientManipulator.delete_row(data["key"], data["value"])
            logger.debug(f'[{request_id}] request done on client option with task_name = {task_name}')
        elif task_name == "select":
            logger.debug(f'[{request_id}] request recived to client option with task_name = {task_name}')
            status = ClientManipulator.get_client(data["user_id"], data["tax_number"])
            logger.debug(f'[{request_id}] request done on client option with task_name = {task_name}')
        elif task_name == "select_all":
            logger.debug(f'[{request_id}] request recived to client option with task_name = {task_name}')
            status = ClientManipulator.get_all_clients(data["user_id"])
            logger.debug(f'[{request_id}] request done on client option with task_name = {task_name}')
        elif task_name == "import":
            logger.debug(f'[{request_id}] request recived to client option with task_name = {task_name}')
            status= ClientManipulator.create_client_with_import(data)
            logger.debug(f'[{request_id}] request done on client option with task_name = {task_name}')
        else:
            status_code = 500
            msg =  f"Couldn't create Traning file for the following reason: " \
                    + f"the task name not valid should be one of those [create, update, delete, select] but we got {task_name}"
            return{
                "status_code":status_code,
                "title":"The task not found",
                "details": msg
            }

        return status