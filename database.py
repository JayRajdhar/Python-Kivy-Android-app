import sqlite3
import pandas as pd
from csv import writer


def create():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='allinfo' ''')

    if cur.fetchone()[0] != 1:
        create_q = 'CREATE TABLE allinfo (id INTEGER PRIMARY KEY, name TEXT, address TEXT, phone TEXT, type TEXT, wt float, gs TEXT, startdate TEXT, enddate TEXT, totalamt TEXT, balamt TEXT, rate TEXT, finalamt TEXT ,settle TEXT)'
        cur.execute(create_q)
        csv_create()

    conn.commit()
    conn.close()

def create_due():
    conn = sqlite3.connect('data_due.db')
    cur = conn.cursor()

    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='dueinfo' ''')

    if cur.fetchone()[0] != 1:
        create_q = 'CREATE TABLE dueinfo (id INTEGER PRIMARY KEY, name TEXT, address TEXT, phone TEXT, startdate TEXT, enddate TEXT, balamt TEXT,reason TEXT, finalamt TEXT ,settle TEXT)'
        cur.execute(create_q)
        csv_create()

    conn.commit()
    conn.close()

def csv_create():
    conn = sqlite3.connect('data.db', isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM allinfo", conn)
    db_df.to_csv('database.csv', index=False)




def insert(namee, address="", phone="", type="", wt="", gs="", startdate="", totalamt="", balamt="", rate="", settle="0"):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    insert_q = 'INSERT INTO allinfo (name, address, phone, type, wt, gs, startdate, totalamt, balamt, rate, settle) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
    cur.execute(insert_q, (namee, address, phone, type, wt, gs, startdate, totalamt, balamt, rate, settle))
    conn.commit()
    conn.close()


def insert_due(namee, address="", phone="", startdate="",balamt="", reason="", settle="0"):
    conn = sqlite3.connect('data_due.db')
    cur = conn.cursor()
    insert_q = 'INSERT INTO dueinfo (name, address, phone, startdate, balamt, reason, settle) VALUES (?,?,?,?,?,?,?)'
    cur.execute(insert_q, (namee, address, phone, startdate, balamt, reason, settle))
    conn.commit()
    conn.close()



def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)


def select():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute('select * from allinfo')
    allq = cur.fetchall()
    conn.close()
    return allq


def search(namee, id):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    search_q = "select * from allinfo where name like ? and id like ?"
    cur.execute(search_q, (namee, id))
    alls = cur.fetchall()
    conn.close()
    return alls

def search_due(namee, id):
    conn = sqlite3.connect('data_due.db')
    cur = conn.cursor()
    search_q = "select * from dueinfo where name like ? and id like ?"
    cur.execute(search_q, (namee, id))
    alls = cur.fetchall()
    conn.close()
    return alls

def search_add(namee,phone):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    search_q = "select * from allinfo where name=? and phone=? "
    cur.execute(search_q, (namee,phone))
    alls = cur.fetchall()
    conn.close()
    return alls


def settle(namee, id, enddate, finalamt):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    settle_q ="update allinfo set settle='1', finalamt =?, enddate=? where name=? and id=?"
    cur.execute(settle_q, (finalamt, enddate, namee, id))
    conn.commit()
    csv_create()
    conn.close()

def settle_due(namee, id, enddate, finalamt):
    conn = sqlite3.connect('data_due.db')
    cur = conn.cursor()
    settle_q ="update dueinfo set settle='1', finalamt =?, enddate=? where name=? and id=?"
    cur.execute(settle_q, (finalamt, enddate, namee, id))
    conn.commit()
    #csv_create()
    conn.close()

def update(namee, phone, address="", type="", wt="", gs="", startdate="", totalamt="", balamt="", rate=""):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    update_q = "update allinfo set address=?, type=?, wt=?, gs=?, startdate=?, totalamt=?, balamt=?, rate=? where name=? and phone=?"
    cur.execute(update_q, (address, type, wt, gs, startdate, totalamt, balamt, rate, namee, phone))
    conn.commit()
    csv_create()
    conn.close()


def update_add(balamt, startdate, namee, idd):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    update_add = "update allinfo set balamt=?, startdate=? where name=? and id=?"
    cur.execute(update_add, (balamt, startdate, namee, idd))
    conn.commit()
    csv_create()
    conn.close()

def due_update_add(balamt, startdate, namee, idd):
    conn = sqlite3.connect('data_due.db')
    cur = conn.cursor()
    update_add = "update dueinfo set balamt=?, startdate=? where name=? and id=?"
    cur.execute(update_add, (balamt, startdate, namee, idd))
    conn.commit()
    #csv_create()
    conn.close()



#print(search('jay%'))
