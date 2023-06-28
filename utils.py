import sqlite3


def get_data(filename,project_id:1):
    relationtype_all = []
    spantype_all = []
    con = sqlite3.connect(filename) 
    cur = con.cursor() 
    try: 
    # 获取所有数据 
        cur.execute("select * from label_types_relationtype")
        relationtype_all = cur.fetchall() 
        cur.execute("select * from label_types_spantype")
        spantype_all = cur.fetchall()
        cur.execute(" select * from \
                    (select * from labels_span where example_id\
                    in (select id from examples_example where project_id = %s) ) l1 \
                    left join label_types_spantype l2 on l1.label_id =  l2.id \
                    left join examples_example l3 on l1.example_id = l3.id\
                    limit 0,500;"%(project_id))
        examples_all = cur.fetchall()
    # print(person_all) 
    # 遍历 
    except Exception as e: 
        print(e) 
        print('查询失败') 
    #print(spantype_all)
    # 关闭游标 
    cur.close() 
    # 关闭连接 
    con.close()
    return relationtype_all,spantype_all,examples_all