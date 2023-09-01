# -*- coding: utf-8 -*- 
import argparse
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
import config as cf
import json
import template as temp
from fa2 import ForceAtlas2
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt

record_txt = {}
nodes,edges,categories = [],[],[]
node_record,category_record,edge_record= [],[],[]

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

def edge_insert(src,dst,type):
    edge_result = {}
    edge_result["source"] = src
    edge_result["target"] = dst
    edge_result["text"] = type
    return edge_result

if __name__ == '__main__':
    forceatlas2 = ForceAtlas2(
                        # Behavior alternatives
                        outboundAttractionDistribution=True,  # Dissuade hubs
                        linLogMode=False,  # NOT IMPLEMENTED
                        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                        edgeWeightInfluence=1.0,

                        # Performance
                        jitterTolerance=1.0,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=1.2,
                        multiThreaded=False,  # NOT IMPLEMENTED

                        # Tuning
                        scalingRatio=2.0,
                        strongGravityMode=False,
                        gravity=10.0,

                        # Log
                        verbose=True)
    
    G = nx.DiGraph()
    parser = argparse.ArgumentParser(prog='scan_vertext_relation.py')
    parser.add_argument('--spacename',type=str,default="f1_news",help='select nebula sapce')
    parser.add_argument('--scan_id',type=str,default="12311",help='the id for scaning vertexs and edges')

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

    client.execute("USE %s"%(opt.spacename))
    result = client.execute(temp.entity_related_template%(opt.scan_id))
    property_m,property_m,property_l ={},{},{}
    for id_m,tag_m,property_m,src_a,dst_a,type_a,id_n,tag_n,property_n,src_b,dst_b,type_b,id_l,tag_l,property_l in result:
        property_n,property_m,property_l = eval(str(property_n)),eval(str(property_m)),eval(str(property_l))
        id_l,id_m,id_n = str(id_l)[1:-1],str(id_m)[1:-1],str(id_n)[1:-1]
        src_a,src_b,dst_a,dst_b,type_a,type_b = str(src_a)[1:-1],str(src_b)[1:-1],str(dst_a)[1:-1],str(dst_b)[1:-1],str(type_a)[1:-1],str(type_b)[1:-1]
        tag_l,tag_m,tag_n = str(tag_l)[2:-2],str(tag_m)[2:-2],str(tag_n)[2:-2]

        if tag_m not in category_record:
            categories.append(category_insert(tag_m,property_m))
        if tag_n not in category_record:
            categories.append(category_insert(tag_n,property_n))
        if tag_l not in category_record:
            categories.append(category_insert(tag_l,property_l))
        if id_m not in node_record:
            nodes.append(nodes_insert(id_m,property_m,category_record.index(tag_m)))
        if id_n not in node_record:
            nodes.append(nodes_insert(id_n,property_n,category_record.index(tag_n)))
        if id_l not in node_record:
            nodes.append(nodes_insert(id_l,property_l,category_record.index(tag_l)))
        if str(src_a)+str(dst_a)+str(type_a) not in edge_record:
            edges.append(edge_insert(src_a,dst_a,type_a))
        if str(src_b)+str(dst_b)+str(type_b) not in edge_record:
            edges.append(edge_insert(src_b,dst_b,type_b))
    
    record_txt["nodes"] = nodes
    record_txt["edges"] = edges
    record_txt["categories"] = categories
    # 添加节点
    for i in record_txt["nodes"]:
        G.add_node(i["id"], name=i["name"], property=i["property"], value=i["value"], category=i["category"])
        print(i["id"])
    # 添加边
    for i in record_txt["edges"]:
        a = i["source"]
        b = i["target"]
        G.add_edge(a, b)
    # 获取节点坐标
    positions = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=2000)
    for i in record_txt["nodes"]:
        i["x"] = positions[i["id"]][0]
        i["y"] = positions[i["id"]][1]
    #print(positions)

    #print(record_txt["nodes"])
    nx.draw_networkx_nodes(G, positions, node_size=20, node_color="blue", alpha=0.4)
    nx.draw_networkx_edges(G, positions, edge_color="green", alpha=0.05)
    plt.axis('off')
    plt.show()
    with open("result.txt","w",encoding="UTF-8") as f:
        json.dump(record_txt,f,ensure_ascii=False,indent=4)
    client.release()

