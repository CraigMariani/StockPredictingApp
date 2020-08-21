'''
The main file for testing the database,
we are using this to call other scripts:

    -database_setup
    -stock_databse
'''

import pymysql
# from database_setup import Database
from stock_database import Database 

if __name__ == '__main__':
    db = Database()

    # db.create_table()

    # db.show_tables()
    
    db.show_contents()


    # db.insert_contents()
