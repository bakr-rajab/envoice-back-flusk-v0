from posixpath import join
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append("/home/frontend/the_accountant/the_accountant/")

from  utilities import Helper
from db_manipulator import DBManipulator
import os
import json
class InitDatabase:
    def __init__(self):
        pass
    @classmethod
    def init_database_seed(cls, db_name, seed_path):
        DBManipulator({"host":"localhost","port":27017})
        tables = []
        unique_attrs = []
        if os.path.isdir(seed_path):
            data, keys = Helper.read_files(seed_path)
            for key in keys:
                for item in data[key]:
                    tables.append(item)
                    unique_attrs.append({item : data[key][item]})
                DBManipulator.create_table(db_name,tables, unique_attrs)
            return True
        else:
            return False


print(InitDatabase.init_database_seed("accountant_db","docs"))