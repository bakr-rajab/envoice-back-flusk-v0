import os
from ..static_table_manipulator import StaticTables
DIR_PATH = os.path.dirname(os.path.realpath(__file__)).replace("flow","")

class StaticDataFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def static_data_handeler(cls,task_name, data= "", unique_value= "" ):

        if task_name == "create":
            status = StaticTables.create_table(os.path.join(DIR_PATH,"docs"))
            if status == True:
                status_code = 200
                return status_code
            else:
                return status
        if task_name == "select":
            status = StaticTables.get_table_with_id(data["table_name"], unique_value)
        elif task_name == "select_all":
            status = StaticTables.get_all_table(data["table_name"])
        elif task_name == "update":
            status = StaticTables.edit_static_table(data["table_name"] ,data,{"code":unique_value})
        elif task_name == "delete":
            status = StaticTables.delete_row(data["table_name"], data["key"], data["value"])
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