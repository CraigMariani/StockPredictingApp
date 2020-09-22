import streamlit as st
import altair as alt

import numpy as np
import pandas as pd
# import time

from stock_database import Database

class Application:

    def __init__(self):
        db = Database()
        df = db.return_contents()

        df_names = pd.read_csv('../data_fetch/robinhood_data/100_most_popular_names.csv')
        df_names.drop(columns=['Unnamed: 0'], inplace=True)

        self.df_names = df_names
        self.df = df
        self.db = db

        

    def predictions(self):
        pass
    
    # lets you choose what stocks you want to check
    def nav_bar(self):
        df = self.df
        df_names = self.df_names

        stock_tickers = list(df.columns)[1:]

        ticker_selected = st.sidebar.selectbox(
            "What Stock would you like to see?",
            (stock_tickers)
        )
        row = df_names.loc[df_names['TickerLabel'] == ticker_selected]
        st.text('Ticker Label: {}  Name: {}'.format(row['TickerLabel'].values[0], row['Name'].values[0]))
        

        return ticker_selected

        # ap.basic_chart(ticker_selected)

    # calling the basic chart to display the stock data
    def basic_chart(self, ticker_selected):
        df = self.df
        # print(df[[ticker_selected]])
        # print(type(df['Date'][0]))
        # stock_chart = alt.Chart(df).mark_line().encode(
        #     x=alt.X(df['Date'], type='temporal'), 
        #     y=alt.Y(df[ticker_selected], type='quantitative') 
        # )

        stock_chart = alt.Chart(df).mark_point().encode(
            # y=ticker_selected,
            # x='Date',
            y=alt.Y(ticker_selected, axis=alt.Axis(format='$', title='Closed Price')),
            x=alt.X('Date', axis=alt.Axis(format='', title='Closed Price')),
        ).properties(
            width=800,
            height=600
        ).configure_mark(
            opacity=0.8
        )
        # st.line_chart(df[[ticker_selected]])
        st.altair_chart(stock_chart)

    def show_data(self):
        df = self.df
        st.write(df.head())

if __name__ == '__main__':
    ap = Application()

    st.title('Stock Predicting App')
    st.write('Predicting Stock Prices with Historical Data From 2015-2020')
    # ap.basic_chart()
    ticker_selected = ap.nav_bar()
    ap.basic_chart(ticker_selected)
