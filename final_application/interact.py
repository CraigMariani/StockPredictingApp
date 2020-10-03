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


    # for closed price table (100_most_popular)
    # db.drop_table()
    # db.create_table()
    # db.insert_contents()
    # db.show_tables()
    # db.show_contents()

    # for names table (ticker_names)
    # db.create_name_table()
    # db.insert_name_contents()

    # for most recent table (most_recent)
    db.get_most_recent()

    # db.show_tables()


    
