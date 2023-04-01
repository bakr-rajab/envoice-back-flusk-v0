
import os
import json
import pandas as pd
from posixpath import join

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
    def get_dates_in_between(cls, start_date, end_date):
        dates_in_between = []
        dates_values = pd.date_range(end_date, start_date)
        print(dates_values)
        date_size = len(dates_values)
        for i in range (date_size):
            dates_in_between.append(str(dates_values[i]).split(" ")[0])
        return dates_in_between