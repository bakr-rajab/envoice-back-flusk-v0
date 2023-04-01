from pymongo import MongoClient

class DBManipulator():
    @classmethod
    def __init__(cls, connections_key):
        cls.client = MongoClient(host=connections_key["host"], port=connections_key["port"])

    @classmethod
    def list_exist_tables(cls, db_name):
        cls.db = cls.client[db_name]
        list_of_collections = cls.db.list_collection_names()
        return list_of_collections
    @classmethod
    def create_session(cls, db_name):
        cls.db = cls.client[db_name]
        return cls.db
    @classmethod
    def create_db(cls, db_name):
        try:
            cls.db = cls.client[db_name]
            return {
                "success":"Done",
                "object":cls.db
            }
        except Exception as ex:
            status_code = 500
            msg = "failed to connect to database for the following reason"+ str(ex)
            return  {
                "status":False,
                "data":{"success":"False",
                "error":{
                    "status_code": status_code,
                    "title":"error on connecting to database",
                    "details": msg
                    }}
                }

    @classmethod
    def create_table(cls, db_name, db_collection_name, unique_attrs):
        result = cls.create_db(db_name)
        if result.get("object"):
            db = result.get("object")
            for _collection_name in db_collection_name:
                collection_name = getattr(db, _collection_name)
                if unique_attrs:
                    for single_unique_attrs in unique_attrs:
                        if _collection_name in single_unique_attrs:
                            for unique_attr in single_unique_attrs[_collection_name]:
                                collection_name.create_index(unique_attr, unique = True)
            return True
        else:
            return "false"

    @classmethod
    def insert_table(cls,  db_collection_name, data):
        collection_name = getattr(cls.db, db_collection_name)
        try:
            if data:
                collection_name.insert_one(data[0]) if len(data) == 1 else collection_name.insert_many(data)
                return True
        except Exception as ex:
            status_code = 500
            msg = f"failed to insert to {db_collection_name} on database {cls.db.name} for the following reason " + str(ex)
            return  {
                "status":False,
                "data":{"success":"False",
                "error":{
                    "status_code": status_code,
                    "title":"error on connecting to database",
                    "details": msg
                    }}
                }

    @classmethod
    def select_query(cls, db_collection_name, query= ""):
        all_data = []
        collection_name = getattr(cls.db, db_collection_name)
        try:
            if query:
                results =  collection_name.find(query)
                for result in results:
                    del result['_id']
                    all_data.append(result)
                return {"status":True,"data":all_data}
            elif not query:
                results = collection_name.find()
                for result in results:
                    del result['_id']
                    if result.get("password"):
                        del result["password"]
                    all_data.append(result)
                return { "status":True, "data":all_data}
            else:
                return {"data":"not a valid option on select from database!!", "status":False}
        except Exception as ex:
            status_code = 500
            msg = f"failed to select from {db_collection_name} on database {cls.db.name} for the following reason " + str(ex)
            return {
                "status":False,
                "data":{"success":"False",
                "error":{
                    "status_code": status_code,
                    "title":"error on connecting to database",
                    "details": msg
                    }}
                }
    # unique value = {"email":"hamdy@gmail.com"}
    @classmethod
    def update_row(cls, db_collection_name, data, unique_value):
        collection_name = getattr(cls.db, db_collection_name)
        old_data = cls.select_query(db_collection_name, unique_value)
        if old_data["status"] == False:
            return { "status":True, "data":f"No record on the data base related to the {db_collection_name} table with this unique value {unique_value}"}
        # try:
        for key1 in old_data["data"][0]:
            for key in data[0]:
                if key1 == key:
                    if data[0][key] != old_data["data"][0][key1]:
                        collection_name.update_one(unique_value, {'$set': {key: data[0][key]}})
        if data[0].get("password"):
            del data[0]["password"]

        return { "status":True, "data":data[0]}

        # except Exception as ex:
        #     status_code = 500
        #     msg = f"failed to update to {db_collection_name} on database {cls.db.name} for the following reason " + str(ex)
        #     return  {
        #         "status":False,
        #         "data":{"success":"False",
        #         "error":{
        #             "status_code": status_code,
        #             "title":"error on connecting to database",
        #             "details": msg
        #             }}
        #         }

    @classmethod
    def delete_row(cls, db_collection_name, column_name, delted_row_val):
        collection_name = getattr(cls.db, db_collection_name)
        try:
            collection_name.delete_one({column_name: delted_row_val})
            return {"status": True, "data": { "deleted_row":delted_row_val}}
        except Exception as ex:
            status_code = 500
            msg = f"failed to delete from {db_collection_name} on database {cls.db.name} for the following reason " + str(ex)
            return  {
                "status":False,
                "data":{"success":"False",
                "error":{
                    "status_code": status_code,
                    "title":"error on connecting to database",
                    "details": msg
                    }}
                }

    @classmethod
    def delete_type_row(cls, db_collection_name, user_id, column_name, delted_row_val):
        collection_name = getattr(cls.db, db_collection_name)
        try:
            collection_name.remove({'user_id':user_id, column_name: delted_row_val})
            return {"status": True, "data": { "deleted_row":delted_row_val}}
        except Exception as ex:
            status_code = 500
            msg = f"failed to delete from {db_collection_name} on database {cls.db.name} for the following reason " + str(ex)
            return  {
                "status":False,
                "data":{"success":"False",
                "error":{
                    "status_code": status_code,
                    "title":"error on connecting to database",
                    "details": msg
                    }}
                }



# if __name__ == "__main__":
# DBManipulator({"host":"localhost","port":27017})
# db = DBManipulator.create_session("accountant_db")

# unique_attrs = {"user":["email","ph_number"], "types":["type_code"], "types_groups": ["group_code"]}
# DBManipulator.create_table("accountant_db",["user","types"],unique_attrs)
#     # DBManipulator.delete_row("sales","ph_number","01113005775")
#     data = [{
#         "name":"mahmoud",
#         "email":"hamad@gmail.com",
#         "ph_number":"515",
#         "password": "1234"
#     }]
#     # print(DBManipulator.update_row("user",data, {"email":"hamada@gmail.com"}))

#     print(DBManipulator.insert_table("user",data))
    # print(DBManipulator.insert_table("user",data))

# print(DBManipulator.select_query("types", {"$and":[{"type_code":1, "user_id":"170474f5030c487c93f59296d99b4def"}]}))