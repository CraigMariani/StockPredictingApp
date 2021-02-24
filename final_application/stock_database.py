'''
database testing again but with the actual data we cleaned and scraped from Robinhood
performs same CRUD operations as database setup, just with actual data we are using

actual data = 100_most_popular_cleaned.csv

'''

import pymysql
# import mysql
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pprint
import datetime


global first_day
global last_day
class Database:

    def __init__(self):

        # reading in csv file of stock data
        df = pd.read_csv('../data_fetch/robinhood_data/100_most_popular_cleaned.csv')

        # reading in csv file of stock ticker names
        df_names = pd.read_csv('../data_fetch/robinhood_data/100_most_popular_names.csv')
        df_names.drop(columns=['Unnamed: 0'], inplace=True)
        userName = None
        passWord = None

        # get login in info for database
        with open('../../LoginCredentials/mysql3.txt') as f:
            file = f.readlines()
            userName = file[0].split('\n')[0]
            passWord = file[1].split('\n')[0]

        # create mysql connection to database with login info
        conn = pymysql.connect(
                                # host="""%admin""",
                                host='localhost', 
                                user=userName, 
                                password=passWord, 
                                db='stock_app')

        # create a currsor with the connection 
        mycursor = conn.cursor()

        # creating mysql engine
        engine = create_engine('mysql+pymysql://{}:{}@localhost/{}'.format(
            userName,
            passWord,
            'stock_app'
        ))
        

        # assigning variables to self for other methods in the class
        self.engine = engine
        self.mycursor = mycursor # the cursor
        self.conn = conn # the connection
        self.df = df # stock data in dataframe
        self.df_names = df_names # tickers with names

        
        self.first_day = df['Date'].iloc[0]
        self.last_day = df['Date'].iloc[-1]
        
        

    # creat the table for stock app
    def create_table(self):

        df = self.df
        ticker_symbols = list(df.columns[1:])

        '''
        ### SQL QUERY SHOULD LOOK SOMETHING LIKE THIS ###

            CREATE TABLE 100_most_popular(
                Date DATE NOT NULL,
                ticker_symbol VARCHAR(8),
                PRIMARY KEY ( Date )

            );
        '''

        # need to make a sql query that will have ticker_symbols for all 100 stock names 
        # try creating a loop that goes through all columns of the dataframe except the first one and append to the end of the python string
        # the string will then be executed as a sql query


        sql = 'CREATE TABLE 100_most_popular( Date DATE NOT NULL, '

        for ticker in ticker_symbols:
            if '.' in ticker:
                ticker_list = ticker.split('.')
                ticker = ticker_list[1]

            sql += ticker
            sql += ' VARCHAR(8), '
        
        sql += 'PRIMARY KEY (Date)  );'

        self.mycursor.execute( self.conn.escape_string(str(sql)))
        self.conn.commit()
    
    
    # look into adding grayscale trust stocks and moderna
    def insert_contents(self):
        df = self.df
        engine = self.engine
        mycursor = self.mycursor
        conn = self.conn
        
        cols_list = []

        # some tickers have periods in their names, formatting it so they are no longer there
        for col in df.columns.tolist():
            if '.' in col:
                col_list = col.split('.')
                col = col_list[1]
            
            cols_list.append(col)

        df.columns = cols_list 
        df.to_sql('100_most_popular', con=engine, if_exists='append', index=False)

    # ticker_name table ###############################################
    # def create_name_table(self):
    #     df_names = self.df_names

    #     # print(df_names.columns)
    #     ticker_symbols = df_names.columns[0]
    #     ticker_names = df_names.columns[1]
        
    #     # print(ticker_symbols)
    #     # print(ticker_names)
    #     sql = '''CREATE TABLE ticker_names( 
    #         symbols VARCHAR(8),
    #         names VARCHAR(8)
    #         )'''
        
    #     self.mycursor.execute(sql)
    #     self.conn.commit()
        
    # for populating the ticker name table
    # def insert_name_contents(self):
    #     df_names = self.df_names
    #     engine = self.engine
    #     mycursor = self.mycursor
    #     conn = self.conn
        

    #     ticker_list = []

    #     # some tickers have periods in their names, formatting it so they are no longer there
    #     for ticker in df_names['TickerLabel'].tolist():
    #         if '.' in ticker:
    #             ticker_list = ticker.split('.')
    #             print(ticker_list)
    #             ticker = ticker_list[1]
            
    #         ticker_list.append(ticker)
    #     print(ticker_list)
    #     df_names['TickerLabel'] = ticker_list
    #     df_names.to_sql('ticker_names', con=engine, if_exists='append', index=False)
    #######################################################################
    # for getting the most recent data table (50 most recent days)
    def get_most_recent(self):

        # returning the most rcent
        # df = pd.read_sql('SELECT * FROM `100_most_popular` ORDER BY  Date DESC LIMIT 37', con=self.conn)
        df = pd.read_sql('SELECT * FROM `100_most_popular` ORDER BY  Date DESC', con=self.conn)   

        df = df.iloc[::-1]
        

        last_day = df['Date'].iloc[-1]
        # last_day = int(last_day)
        # print(type(last_day))

        first_day = df['Date'].iloc[0]
        # first_day = int(first_day)
        # print(type(first_day))

        df['Date'] = np.arange(1,len(df['Date']) + 1)
        
        for col in df.columns[1:]:
            df[col] = df[col].astype(float)

        # return df, first_day, last_day

        
        return df
    
    def get_dates(self):
        return self.first_day, self.last_day
    ######################################################################
     
    def drop_table(self):
        self.mycursor.execute('DROP TABLE `100_most_popular`')
        self.conn.commit()

    def delete_contents(self):
        self.mycursor.execute('DELETE FROM `100_most_popular`')
        self.conn.commit()

    def show_tables(self):
        self.mycursor.execute('SHOW TABLES;')
        # self.conn.commit()
        for i in self.mycursor.fetchall():
            print(i)
    

    def show_contents(self):
        self.mycursor.execute('SELECT * FROM 100_most_popular')
        # self.mycursor.execute('SELECT * FROM ticker_names')
        # self.conn.commit()
        for i in self.mycursor.fetchall():
            print(i)

    # returns contents in pandas dataframe
    def return_contents(self):
        
        df2 = pd.read_sql('SELECT * FROM 100_most_popular', con=self.conn)
        df2['Date'] = pd.to_datetime(df2['Date'])
        for col in df2.columns[1:]:
            df2[col] = df2[col].astype(float)
        # print(df2.info())
        # print(df2.head())
        return df2
        