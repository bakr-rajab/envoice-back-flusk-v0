
import pandas as pd
def read_csv_file(file_path, key_validators):
    df = pd.read_csv(file_path)
    keys = df.columns.to_list()
    if keys == key_validators:
        print("hi")
    else:
        print(list(set(key_validators) - set(keys)))


read_csv_file("train.csv", [ 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'])