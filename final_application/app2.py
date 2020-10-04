import streamlit as st
import altair as alt
# import plotly.express as px
# import plotly.graph_objects as go

import numpy as np
import pandas as pd
# import time
import matplotlib.pyplot as plt
import seaborn as sns

from poly_regression import Regression
from stock_database import Database

class Application():

    def __init__(self):
        db = Database()
        df = db.return_contents()

        df_names = pd.read_csv('../data_fetch/robinhood_data/100_most_popular_names.csv')
        df_names.drop(columns=['Unnamed: 0'], inplace=True)

        self.df_names = df_names
        self.df = df
        self.db = db
    
    # lets you choose what stocks you want to check
    def nav_bar(self):
        df = self.df
        df_names = self.df_names

        stock_tickers = list(df.columns)[1:]

        ticker_selected = st.sidebar.selectbox(
            "What Stock would you like to see?",
            (stock_tickers)
        )

        n_values = np.arange(0, 10)
        n = st.sidebar.selectbox(
            "Select n for the complexity of the polynomial",
            (n_values)
        )


        row = df_names.loc[df_names['TickerLabel'] == ticker_selected]
        st.text('Ticker Label: {}  Name: {}'.format(row['TickerLabel'].values[0], row['Name'].values[0]))
        
        return ticker_selected, n
    
   
    def make_prediction(self, ticker_selected, n):
        re = Regression(ticker_selected, n)
        db = Database()
        re.train()
        close_out, close_test = re.test()

        poly_rmse = re.calculate_error(close_out)
        st.sidebar.text('Mean Squared Error: {}'.format(poly_rmse))
        
        poly_rs = re.calculate_accuracy(close_out)
        st.sidebar.text('R Squared Score (Accuracy): {}'.format(poly_rs))
        

        close_test1d = close_test.flatten()
        close_out1d = close_out.flatten()
        data_close = [close_test1d, close_out1d]

        df_close = pd.DataFrame({ 'Real' : close_test1d, 'Predicted' :  close_out1d })
        st.sidebar.text(df_close)

        first_day, last_day = db.get_dates()
        
        st.sidebar.text('{} to {}'.format(first_day, last_day))

        #### showing the new predictions 
        future_days, future_closed_prices = re.show_predictions()
        st.sidebar.text('Stock ten days ahead')
        df_future = pd.DataFrame({ 'Future Days' : future_days, 'Future Closed Prices' :  future_closed_prices })
        st.sidebar.text(df_future)

        date_train, date_test, close_train, close_test = re.get_train_test_data()
        
        return close_out, date_test
    
    

    # simpler way to plot dataframes
    def plot_dfs(self, dfs, labels):

        for i, df in enumerate(dfs):
            stock_chart = alt.Chart(df).mark_line().encode(
                y=alt.Y(labels[i], axis=alt.Axis(format='$', title=labels[i])),
                x=alt.X('Day', axis=alt.Axis(format='', title='Day')),
            ).properties(
                width=800,
                height=300
            ).configure_line(
                opacity=0.8
            )
            # st.line_chart(df[[ticker_selected]])
            st.altair_chart(stock_chart)
        
    # compacting the data into dataframes
    def format_dfs(self, ticker_selected, close_out, date_test):
        db = self.db
        df = db.get_most_recent()

        close_out1d = close_out.flatten()
        close_out1d.sort()
        

        date_test1d = date_test.flatten()
        date_test1d.sort()
       
        df_predicted = pd.DataFrame({ 'Day' : np.array(date_test1d), 'Predicted' :  close_out1d })
        df_predicted.set_index('Day')
        
        
        # orginal values dataframe
        df_original = pd.DataFrame({ 'Day' : df['Date'], 'Original' : df[ticker_selected]})
        df_original.set_index('Day')
        
        return df_original, df_predicted

    def show_learning_curves(self, ticker_selected, n):
        re = Regression(ticker_selected, n)

        train_errors, val_errors = re.learning_curves(n)

        df_errors = pd.DataFrame({ 'Train Errors ' : np.sqrt(train_errors), 'Val Errors' : val_errors})

        st.line_chart(data=df_errors, width=800, height=300)



if __name__ == '__main__':
    ap = Application()

    st.title('Stock Predicting App')
    
    ticker_selected, n = ap.nav_bar()
    
    
    st.text('Predicting Stock Prices with Historical Data')
    
    close_out, date_test = ap.make_prediction(ticker_selected, n) # returns predicted values 

    # ap.most_recent(ticker_selected, close_out, date_test) # displays most recent data

    df_original, df_predicted = ap.format_dfs(ticker_selected, close_out, date_test) # df converter
    dfs = [df_original, df_predicted]
    labels = ['Original', 'Predicted']
    
    ap.plot_dfs(dfs, labels)
    
    if st.sidebar.checkbox('Show Learning Curves'):
        ap.show_learning_curves(ticker_selected, n)


    

 