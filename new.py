import time 
import template as temp
"""
创建图空间基本信息的函数
"""
def create_DB_space(client,spacename):
    client.execute(temp.drop_space_template%(spacename))
    client.execute(temp.create_space_template%(spacename))
    time.sleep(10)
    client.execute(" USE %s;"%(spacename))

def create_TAG_RELATION(client,span,relation):
    #create TAG
    for sp in span:
        #print(sp)
        if sp[10]==0:
            #print("CREATE TAG IF NOT EXISTS `%s`(name string,ground_color string DEFAULT \"%s\",text_color string DEFAULT \"%s\");"%(sp[1],sp[4],sp[5]))
            client.execute(temp.create_TAG_template%(sp[1],sp[4],sp[5]))
    #create relation
    for rel in relation:
        #print("CREATE EDGE IF NOT EXISTS `%s`(rel_type int DEFAULT 0,name string DEFAULT \"%s\",ground_color string DEFAULT \"%s\",text_color string DEFAULT \"%s\");"%(rel[1],rel[1],rel[4],rel[5]))
        client.execute(temp.create_EDGE_template%(rel[1],rel[1],rel[4],rel[5]))

def Delete_Space(client,spacename):
    client.execute(temp.drop_space_template%(spacename))
