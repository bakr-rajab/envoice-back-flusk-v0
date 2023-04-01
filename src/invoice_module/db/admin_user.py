import sys
from db_manipulator import DBManipulator
from getpass import getpass
from passlib.hash import pbkdf2_sha256
import uuid
class Admin:

    @classmethod
    def __init__(cls):
        pass
    @classmethod
    def create_admin(cls, tax_number, password, name):
        data = {}
        data["user_id"] = uuid.uuid4().hex
        data['password'] = pbkdf2_sha256.hash(password)
        data["tax_number"] = tax_number
        data['name'] = name
        data["user_role"] = "admin"
        result = DBManipulator.insert_table("user",[data])
        if result == True:
            del data["password"]
            del data["_id"]
            output = {"status":True, "data":data}
        else:
            output = {"status":False, "data":result}
        return output

    @classmethod
    def delete_admin(cls, key, value):
        result = DBManipulator.delete_row("user",key,value)
        if result["status"] == True:
            output = {"status":True, "data":{key:value}}
        else:
            output = {"status":False, "data":result}
        return output
def main():
    DBManipulator({"host":"localhost","port":27017})
    db = DBManipulator.create_session("accountant_db")
    if sys.argv[1] == "create":
        __name = input("Enter name:  ")
        __tax_number = int(input("Enter tax_number:  "))
        __password = getpass("Enter password:  ")
        print(Admin.create_admin(__tax_number, __password, __name))
    elif sys.argv[1] == "delete":
        __tax_number = input("Enter tax_number: ")
        print(Admin.delete_admin("tax_number", __tax_number))

main()

