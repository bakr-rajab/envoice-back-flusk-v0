from ..types_manipulator import TypeManipulator


class TypesFlow:
    @classmethod
    def __init__(cls) -> None:
        pass
    @classmethod
    def types_handeler(cls,task_name, data= "", unique_value= "" ):

        if task_name == "create":
            status= TypeManipulator.create_type(data)
        elif task_name == "update":
            status = TypeManipulator.edit_type(data,{"type_code":unique_value})
        elif task_name == "delete":
            status = TypeManipulator.delete_row("types",data["user_id"],data["key"], data["value"])
        elif task_name == "select":
            status = TypeManipulator.get_type(data["type_code"],data["user_id"])
        elif task_name == "select_all":
            status = TypeManipulator.get_all_types(data["user_id"])
        elif task_name == "import":
            status = TypeManipulator.create_types_with_import(data)
        else:
            status_code = 500
            msg =  f"Couldn't recognize the type " \
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