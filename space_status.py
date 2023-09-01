import sqlite3
import os
#Space_Status_Template = "select * from label_types_relationtype where project_id = 6"
Space_Status_Template = "select grpah_imported from projects_project where projects_project.id = %s"
msg = ["未导入","已导入","待更新"]


if __name__ == '__main__':
    result = {}
    path = os.getcwd()
    file = path + "\db.sqlite3"
    con = sqlite3.connect(file)
    cur = con.cursor() 
    try:
        #cur.execute(temp.Space_Status_Template%(project_id))
        cur.execute(Space_Status_Template%("6"))
        examples = cur.fetchall()
        result["statusCode"] = int(examples[0][0])
        result["statusMsg"] = msg[int(examples[0][0])]
    except Exception as e: 
        print(e) 
        print('查询失败')   
    print(result)