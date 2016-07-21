import sqlite3 as lite

conn = lite.connect('pepto.db')
print ("Opened database succesfully");
with conn:
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS survey')
    conn.execute('CREATE TABLE Survey(ID INTEGER PRIMARY KEY,'
                  'account CHAR(2) NOT NULL,handle CHAR(50) NOT NULL,gender CHAR(2) NOT NULL,'
                  'age CHAR (3) NOT NULL,education CHAR(2) NOT NULL,houseHoldIncome CHAR(2) NOT NULL,'
                  'favoriteFoods CHAR(2) NOT NULL,employed CHAR(2) NOT NULL,publicWork CHAR(2) NOT NULL,'
                   'zipcode CHAR (10) NOT NULL,status CHAR(2) NOT NULL,ethnicity CHAR(2) NOT NULL)')
    print ("Table created successfully")

conn.close()