import os
import sqlite3
project_id = 12
path = os.getcwd()
# file = path + "\db1.sqlite3"
file ="D:/label/TextLabelingBasedOnDoccano/backend/db.sqlite3"
con = sqlite3.connect(file) 
cur = con.cursor() 
try:
    print(project_id)
    cur.execute("update projects_project set grpah_imported = 2 where  grpah_imported = 1")
    con.commit()
    examples_all = cur.fetchall()
    print(examples_all)
except Exception as e:
    print(e) 
    print('查询失败')   