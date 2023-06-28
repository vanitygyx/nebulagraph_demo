import time 
"""
创建图空间基本信息的函数
"""
def create_DB_space(client,spacename):
    client.execute('CREATE SPACE IF NOT EXISTS %s(vid_type=FIXED_STRING(32));'%(spacename))
    time.sleep(10)
    client.execute(" USE %s;"%(spacename))

def create_TAG_RELATION(client,span,relation):
    #create TAG
    for sp in span:
        #print(sp)
        if sp[10]==0:
            client.execute("CREATE TAG IF NOT EXISTS `%s`();"%(sp[1]))
    #create relation
    for rel in relation:
        client.execute("CREATE EDGE IF NOT EXISTS `%s`(rel_type int DEFAULT 0);"%(rel[1]))