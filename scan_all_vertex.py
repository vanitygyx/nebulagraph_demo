import argparse
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
import config as cf
import template as temp
import json
from operator import itemgetter
record_txt = {}
nodes,categories,edges = [],[],[]
node_record,category_record= [],[]

def category_insert(tag,property):
    category_record.append(tag)
    category_result = {}
    category_result["name"] = tag
    category_result["itemStyle"] = {"ground_color":property["ground_color"]}
    category_result["label"] = {"color":property["text_color"]}
    return category_result

def nodes_insert(id,property,num):
    node_record.append(id)
    node_result = {}
    node_result["id"] = id
    node_result["name"] = id
    node_result["value"] = property["name"]
    node_result["property"] = {}
    node_result["category"] = num
    return node_result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='scan_vertext_relation.py')
    parser.add_argument('--spacename',type=str,default="f1_news",help='select nebula sapce')
    
    page = 1
    opt = parser.parse_args()
    spacename = opt.spacename

    config = Config()
    config.max_connection_pool_size = 2
    # init connection pool
    connection_pool = ConnectionPool()
    
    # get session from the pool
    status = connection_pool.init([(cf.addr, cf.port)], config)
    client = connection_pool.get_session(cf.usr, cf.pwd)
    assert client is not None

    respond = client.execute("USE %s"%(opt.spacename))
    result = client.execute(temp.all_entities_template%((page-1)*500,page*500))
    property_v = {}
    for id_v,tag_v,property_v in result:
        property_v = eval(str(property_v))
        id_v = str(id_v)[1:-1]
        tag_v = str(tag_v)[2:-2]
        if tag_v not in category_record:
            categories.append(category_insert(tag_v,property_v))
        if id_v not in node_record:
            nodes.append(nodes_insert(id_v,property_v,category_record.index(tag_v)))
    nodes.sort(key=itemgetter("category"))

    record_txt["nodes"] = nodes
    record_txt["edges"] = edges
    record_txt["categories"] = categories
    connection_pool.close()
    
    print(record_txt)

    with open("result_all_vertex.txt","w",encoding="UTF-8") as f:
        json.dump(record_txt,f,ensure_ascii=False,indent=4)