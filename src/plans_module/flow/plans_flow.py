from ..plans_manipulator import PlansManipulator


class PlansFlow:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def plan_handeler(cls,task_name, data= "", unique_value= "" ):
        if task_name == "create":
            status= PlansManipulator.create_plan(data)
        elif task_name == "update":
            status = PlansManipulator.edit_plans(data,{"plan_id":unique_value})
        elif task_name == "delete":
            status = PlansManipulator.delete_row(data["key"], data["value"])
        elif task_name == "select":
            status = PlansManipulator.get_plans(data["plan_id"])
        elif task_name == "select_all":
            status = PlansManipulator.get_all_plans()
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