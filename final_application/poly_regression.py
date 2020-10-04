'''
The purpose of this class is to use Polynomial Regression to predict new stock prices with the current selected stock

1) There will be a drop down/text box and the user can decide what n will be for the ml model 
2) User selects n value and the line is graphed on the scatter plot of the stock
3) The output will be the predicted values y (closed price) based on the x values (days) and will match the training values depending on n
4) There will also be a confidence score that will determine the accuracy 
5) Learning curves and hard data will also be displayed for the output

'''


# standard datascience libraries
import numpy as np
import pandas as pd

# machine learning set up
from sklearn.model_selection import train_test_split 
from sklearn.pipeline import make_pipeline

# machine learning libraries
from sklearn.linear_model import Ridge
# from sklearn.linear_model import ElasticNet
# from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# reporting the errors and checking accuracy 
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# communicating with mysql database
from stock_database import Database

class Regression():

    # constructor function
    def __init__(self, ticker_selected, n):
        db = Database()

        df = db.get_most_recent()

        # preprocessing the date and the selected data int matricies 
        date = np.array(df['Date']).reshape(-1, 1)
        close = np.array(df[ticker_selected]).reshape(-1, 1)

        # splitting the data
        date_train, date_test, close_train, close_test = train_test_split(date, close, test_size=0.30, random_state=42)
        
        # initialization 
        self.date_train = date_train
        self.close_train = close_train

        self.date_test = date_test
        self.close_test = close_test

        # creating model 
        poly_model = make_pipeline(PolynomialFeatures(n), Ridge())

        self.poly_model = poly_model
        self.date = date

    def show_predictions(self):
        date = self.date
        date = date.flatten()
        latest = date[len(date) - 1]

        future_days = np.arange(latest, latest+10, 1)
        future_days = future_days.reshape(-1, 1)

        poly_model = self.poly_model

        future_closed_prices = poly_model.predict(future_days)

        future_days = future_days.flatten()
        future_closed_prices = future_closed_prices.flatten()
        return future_days, future_closed_prices

    def get_train_test_data(self):
        return self.date_train, self.date_test, self.close_train, self.close_test

    def get_dates(self):
        return self.first_day, self.last_day

    def train(self):
        poly_model = self.poly_model
        
        date_train = self.date_train
        close_train = self.close_train

        poly_model.fit(date_train, close_train)
        

    def test(self):
        poly_model = self.poly_model
        date_test = self.date_test
        date_train = self.date_train
        close_test = self.close_test

        close_out = poly_model.predict(date_test)

        return close_out, close_test
    
    # taking mean squared error of predictions usually 0-1
    def calculate_error(self, close_out):
        close_test = self.close_test

        # y true - y predicted  
        # the output is in closed price, this determines how much off the price is 
        return np.sqrt(mean_squared_error(close_test, close_out))

    # returns R squared (coefficent of determination) usually 0-1
    def calculate_accuracy(self, close_out):
        close_test = self.close_test

        # y true - y predicted  
        # the output is in closed price, this determines how accurate the predicted price is
        return r2_score(close_test, close_out)
    
    # plot the learning curves of the model using mean squared error
    def learning_curves(self, n):
        # creating model 
        poly_model = make_pipeline(PolynomialFeatures(n), Ridge())

        date_val = self.date_test
        date_train = self.date_train
        close_val = self.close_test
        close_train = self.close_train

        train_errors, val_errors = [], []

        for m in range(1, len(date_train)):
            poly_model.fit(date_train[:m], close_train[:m])

            close_train_predict = poly_model.predict(date_train[:m])
            close_val_predict = poly_model.predict(date_val)

            train_errors.append(mean_squared_error(close_train[:m], close_train_predict))
            val_errors.append(mean_squared_error(close_val, close_val_predict))

        return train_errors, val_errors

