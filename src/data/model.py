import numpy as np
from pandas.api.types import CategoricalDtype

from sklearn import linear_model
from sklearn import preprocessing

from sklearn.externals.joblib import dump, load

import data.mpg as mpg

model_path = '../output/model.output'
makes_path = '../output/makes.output'

def predict(df):
    model = load(model_path)
    makes = load(makes_path)

    le = preprocessing.LabelEncoder()
    le.fit(makes)

    df['car_make'] = le.transform(df['car_make'])
    targets = ['mpg']

    feature_names = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'car_make']
    X = df.filter(items=feature_names)

    return model.predict(X)

def train_model(file_path):
    df = mpg.read_cars(file_path)
    feature_names = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'car_make']
    makes = np.sort(df.car_make.unique())

    le = preprocessing.LabelEncoder()
    le.fit(makes)

    df['car_make'] = le.transform(df['car_make'])
    targets = ['mpg']
    
    X = df.filter(items=feature_names)
    y = df['mpg']
    lm = linear_model.LinearRegression()
    model = lm.fit(X,y)

    dump(model, model_path)
    dump(makes, makes_path)