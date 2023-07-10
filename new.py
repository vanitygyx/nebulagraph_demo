import time 
"""
创建图空间基本信息的函数
"""
def create_DB_space(client,spacename):
    client.execute('CREATE SPACE IF NOT EXISTS %s(vid_type=FIXED_STRING(256));'%(spacename))
    time.sleep(10)
    client.execute(" USE %s;"%(spacename))

def create_TAG_RELATION(client,span,relation):
    #create TAG
    for sp in span:
        #print(sp)
        if sp[10]==0:
            client.execute("CREATE TAG IF NOT EXISTS `%s`(name string,ground_color string DEFAULT %s,text_color string DEFAULT %s);"%(sp[1],sp[4],sp[5]))
    #create relation
    for rel in relation:
        client.execute("CREATE EDGE IF NOT EXISTS `%s`(rel_type int DEFAULT 0,name string DEFAULT %s,ground_color string DEFAULT %s,text_color string DEFAULT %s);"%(rel[1],rel[1],rel[4],rel[5]))

def Delete_Space(client,spacename):
    client.execute("DROP SPACE IF EXISTS %s;"%(spacename))
