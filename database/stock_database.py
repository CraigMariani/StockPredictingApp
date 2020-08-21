'''
database testing again but with the actual data we cleaned and scraped from Robinhood
performs same CRUD operations as database setup, just with actual data we are using

actual data = 100_most_popular_cleaned.csv

'''

import pymysql
import pandas as pd
from sqlalchemy import create_engine
import pprint
import datetime

class Database:

    def __init__(self):

        # reading in csv file of stock data
        df = pd.read_csv('../data_fetch/robinhood_data/100_most_popular_cleaned.csv')

        userName = None
        passWord = None

        # get login in info for database
        with open('../../LoginCredentials/mysql.txt') as f:
            file = f.readlines()
            userName = file[0].split('\n')[0]
            passWord = file[1].split('\n')[0]

        # create mysql connection to database with login info
        conn = pymysql.connect(host='localhost', 
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

        
    
    
    def drop_table(self):
        pass
    
    def show_tables(self):
        self.mycursor.execute('SHOW TABLES;')
        # self.conn.commit()
        for i in self.mycursor.fetchall():
            print(i)
    

    def show_contents(self):
        self.mycursor.execute('SELECT * FROM 100_most_popular')
        # self.conn.commit()
        for i in self.mycursor.fetchall():
            print(i)
