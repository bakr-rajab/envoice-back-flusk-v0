from ..license_engine import LicenseManipulator
class LicenseFlow:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def license_handeler(cls,task_name, data= "", unique_value= "" ):
        if task_name == "create":
            status= LicenseManipulator.create_license(data)
        elif task_name == "update":
            status = LicenseManipulator.edit_license(data,{"license_id":unique_value})
        elif task_name == "delete":
            status = LicenseManipulator.delete_row(data["key"], data["value"])
        elif task_name == "select":
            status = LicenseManipulator.get_license(data["license_id"])
        elif task_name == "select_all":
            status = LicenseManipulator.get_all_license()
        elif task_name == "check":
            status = LicenseManipulator.check_license(data["user_id"])
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