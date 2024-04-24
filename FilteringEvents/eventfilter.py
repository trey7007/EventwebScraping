import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

sqlite_db = './eventdata.db'
conn = sqlite3.connect(sqlite_db)
conn.row_factory = dict_factory
c = conn.cursor()

with open('./FilteringEvents/eventfiltering.sql','r') as f:
    sql = f.read() 
    c.execute(sql)
    res = c.fetchall()

    with open('./FilteringEvents/filteredevents.json', 'w') as w:
        w.write(json.dumps(res))
