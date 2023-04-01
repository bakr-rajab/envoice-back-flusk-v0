from ..types_manipulator import TypeManipulator


class TypesGroupsFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def types_groups_handeler(cls,task_name, data= "", unique_value= "" ):
        if task_name == "create":
            status= TypeManipulator.create_type_group(data)
        elif task_name == "update":
            status = TypeManipulator.edit_types_group(data,{"group_code":unique_value})
        elif task_name == "delete":
            status = TypeManipulator.delete_row("types_groups",data["user_id"], data["key"], data["value"])
        elif task_name == "select":
            status = TypeManipulator.get_type_group(data["group_code"],data["user_id"])
        elif task_name == "select_all":
            status = TypeManipulator.get_all_type_group(data["user_id"])
        elif task_name == "import":
            status= TypeManipulator.create_types_group_with_import(data)
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