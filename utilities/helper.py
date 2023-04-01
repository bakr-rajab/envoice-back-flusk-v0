
import os
import json
import pandas as pd

class Helper:
    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def read_files(cls, rootdir):
        data = {}
        files_data = []
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".json"):
                    with open(filepath) as outfile:
                        data[filepath.split("/")[-1].replace('.json','')] = json.load(outfile)
                    files_data.append(filepath.split("/")[-1].replace('.json',''))
        return data, files_data


    @classmethod
    def read_csv_file(cls, data_frame, key_validators):
        f = open("utilities/conf/validators.json")
        json_data = json.load(f)
        null_data = []
        df = data_frame
        keys = df.columns.to_list()
        if not df[df.isna().any(axis=1)].empty:
            null_rows = df[df.isna().any(axis=1)]
            null_rows = null_rows.fillna('')
            null_rows = null_rows.reset_index()  # make sure indexes pair with number of rows
            for index, row in null_rows.iterrows():
                null_data.append(dict(row))
            return {"status": False,"reason":"Some records has no values check records below !!", "data":null_data}
        elif keys == json_data[key_validators]:
            return {"status": True, "data":df}
        else:
            return {"status": False,"reason": "Keys not valid check needed keys below !!", "data":list(set(key_validators) - set(keys))}
    @classmethod
    def get_dates_in_between(cls, start_date, end_date):
        dates_in_between = []
        dates_values = pd.date_range(end_date, start_date)
        date_size = len(dates_values)
        for i in range (date_size):
            dates_in_between.append(str(dates_values[i]).split(" ")[0])
        return dates_in_between