import pandas as pd
from pandas.io.json import json_normalize

def read_cars(file_path):
    df = pd.read_fwf(file_path)
    setup_dataframe(df)
    return df

def read_cars_from_json(json_data):
    df = json_normalize(json_data)
    format_dataframe(df)
    return df

def setup_dataframe(df):
    # add columns
    df.columns = [
        "mpg", "cylinders", "displacement",
        "horsepower", "weight", "acceleration",
        "model_year", "origin", "car_name"
    ]

    format_dataframe(df)

def format_dataframe(df):
    # remove quotes
    df['car_name'] = df.car_name.str.replace('"', '')

    # fix 'chevroelt' typo
    df['car_name'] = df.car_name.str.replace('chevroelt', 'chevrolet')

    # fix 'toyouta' typo
    df['car_name'] = df.car_name.str.replace('toyouta', 'toyota')

    # fix 'maxda' typo
    df['car_name'] = df.car_name.str.replace('maxda', 'mazda')

    # Change 'chevy' to full name
    df['car_name'] = df.car_name.str.replace('chevy', 'chevrolet')

    # create column for vehicle make
    df['car_make'] = df.car_name.str.replace(r'^([^ ]+) .*$', r'\1')