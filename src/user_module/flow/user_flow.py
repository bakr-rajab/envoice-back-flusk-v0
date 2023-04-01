import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/")
from ..user import User

class UserFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def user_handeler(cls,task_name, data= "", unique_value= "" ):
        if task_name == "create":
            status = User.create_user(data)
        elif task_name == "update":
            status = User.edite_user(data,{"tax_number":unique_value})
        elif task_name == "delete":
            status = User.delete_row(data["key"], data["value"])
        elif task_name == "select":
            status = User.get_user(data["user_id"])
        elif task_name == "select_all":
            status = User.get_all_users()
        elif task_name == "auth":
            status = User.authinticate_user(data["tax_number"], data["password"])

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