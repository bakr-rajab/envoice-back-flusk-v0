from ..branch_manipulator import BranchManipulator

from utilities.logger_settings import LoggerSettings

class BranchFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def branch_handeler(cls,task_name, request_id, data= "", unique_value= "" , ):
        logger, _ = LoggerSettings.logger_setting()
        logger.debug(f'[{request_id}] request recived to branch option')
        if task_name == "create":
            logger.debug(f'[{request_id}] request recived to branch option with task_name = {task_name}')
            status= BranchManipulator.create_branch(data)
            logger.debug(f'[{request_id}] request done on branch option with task_name = {task_name}')
        elif task_name == "update":
            logger.debug(f'[{request_id}] request recived to branch option with task_name = {task_name}')
            status = BranchManipulator.edit_branch(data,{"branch_code":unique_value})
            logger.debug(f'[{request_id}] request done on branch option with task_name = {task_name}')
        elif task_name == "delete":
            logger.debug(f'[{request_id}] request recived to branch option with task_name = {task_name}')
            status = BranchManipulator.delete_row(data["user_id"], data["key"], data["value"])
            logger.debug(f'[{request_id}] request done on branch option with task_name = {task_name}')
        elif task_name == "select":
            logger.debug(f'[{request_id}] request recived to branch option with task_name = {task_name}')
            status = BranchManipulator.get_branch(data["branch_code"],data["user_id"])
            logger.debug(f'[{request_id}] request done on branch option with task_name = {task_name}')
        elif task_name == "select_all":
            logger.debug(f'[{request_id}] request recived to branch option with task_name = {task_name}')
            status = BranchManipulator.get_all_branches(data["user_id"])
            logger.debug(f'[{request_id}] request done on branch option with task_name = {task_name}')
        elif task_name == "import":
            logger.debug(f'[{request_id}] request recived to branch option with task_name = {task_name}')
            status= BranchManipulator.create_branch_with_import(data)
            logger.debug(f'[{request_id}] request done on branch option with task_name = {task_name}')
        else:
            status_code = 500
            msg =  f"Couldn't create Traning file for the following reason: " \
                    + f"the task name not valid should be one of those [create, update, delete, select] but we got {task_name}"
            return{
                "status_code":status_code,
                "title":"The task not found",
                "details": msg
            }
        if status == True:
                status_code = 200
                return status_code
        else:
                return status