''' 
used for setting up the database 
    -initial connection (start_database)
    -selecting the database (start_database)

used for testing database 
    -creating tables if needed (create_table) CREATE
    -checking if we can query data (query_table) READ
    -inserting values into tables (insert_into_table) UPDATE
    -dropping tables (drop_table) DELETE
    -deleting data from a table (delete_from_table) DELETE

'''

import pymysql

class Database:

    # database setup
    # constructor / called every time
    def __init__(self):
        userName = None
        passWord = None

        with open('../../LoginCredentials/mysql.txt') as f:
            file = f.readlines()
            userName = file[0].split('\n')[0]
            passWord = file[1].split('\n')[0]


        conn = pymysql.connect(host='localhost', 
                                user=userName, 
                                password=passWord, 
                                db='stock_app')


        mycursor = conn.cursor()
        
        self.mycursor = mycursor # the cursor
        self.conn = conn # the connection


    ###### testing database ######

    # CREATE
    def create_table(self):
        sql = '''CREATE TABLE test_table(
                    stock_id INT NOT NULL AUTO_INCREMENT,
                    stock_name VARCHAR(33) NOT NULL,
                    closed_price INT NOT NULL,
                    date DATE,
                    PRIMARY KEY (stock_id) 
                    );'''

        self.mycursor.execute(sql)
        self.conn.commit()

    # READ (tables)
    def view_tables(self):
        self.mycursor.execute('SHOW TABLES;')
        
        for i in self.mycursor:
            print(i)

    # READ (contents of test table)
    def view_contents(self):
        self.mycursor.execute('SELECT * FROM test_table;')
        for i in self.mycursor.fetchall():
            print(i)
    
    # UPDATE (insert data into a table)
    def insert_into_table(self):
        sql = '''INSERT INTO test_table (stock_name, closed_price, date)
                VALUES ('Apple', 580, '2020-08-15'),
                        ('Google', 900, '2020-08-15');
                ''' 

        self.mycursor.execute(sql)
        self.conn.commit()

    # DELETE (delete elements from table)
    def delete_from_table(self):
        sql = ''' DELETE FROM test_table
                WHERE stock_name = 'Apple';
        '''

        self.mycursor.execute(sql)
        self.conn.commit()
    
    # DELETE (drop the test table)
    def drop_table(self):
        
        self.mycursor.execute('DROP TABLE test_table;')
        self.conn.commit()