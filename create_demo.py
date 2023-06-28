import argparse
import sqlite3
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
from nebula3.common import *
import json
import time

def get_data(filename):
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
    return relationtype_all,spantype_all

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='create_demo.py')
    parser.add_argument('--file',default='db.sqlite3',help='load DB file')
    parser.add_argument('--spacename',type=str,default="test",help='select nebula sapce')
    opt = parser.parse_args()
    #print(opt)
    relation,span = get_data(opt.file)
    spacename = opt.spacename
    print(spacename)
    try:
        config = Config()
        config.max_connection_pool_size = 2
        # init connection pool
        connection_pool = ConnectionPool()
        assert connection_pool.init([('172.27.208.1', 9669)], config)
        # get session from the pool
        client = connection_pool.get_session('root', 'nebula')
        assert client is not None

        # get the result in json format
        resp_json = client.execute_json("yield 1")
        json_obj = json.loads(resp_json)
        print(json.dumps(json_obj, indent=2, sort_keys=True))
        
        # create DB space 
        client.execute('CREATE SPACE IF NOT EXISTS %s(vid_type=FIXED_STRING(32));'%(spacename))
        #time.sleep(20)
        client.execute(" USE %s;"%(spacename))
        span_property = {}

        #create TAG
        for sp in span:
            if sp[10]==1:
                #print(sp[1])
                if sp[9] in span_property:
                    span_property[sp[9]]+=',`%s` string'%(sp[1])
                else:
                    span_property[sp[9]] = '`%s` string'%(sp[1])
        for sp in span:
            #print(sp)
            if sp[10]==0:
                if sp[0] in span_property:
                    print("CREATE TAG IF NOT EXISTS `%s`(%s);"%(sp[1],span_property[sp[0]]))
                    client.execute("CREATE TAG IF NOT EXISTS `%s`(%s);"%(sp[1],span_property[sp[0]])) 
                else:
                    client.execute("CREATE TAG IF NOT EXISTS `%s`();"%(sp[1]))
        #create relation
        for rel in relation:
            client.execute("CREATE EDGE IF NOT EXISTS `%s`(rel_type int DEFAULT 0);"%(rel[1]))
    except Exception as x:
        import traceback
        print(traceback.format_exc())
        if client is not None:
            client.release()
        exit(1)