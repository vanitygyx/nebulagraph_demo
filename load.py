import argparse
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
from nebula3.common import *
import logging
import time
from utils import get_tag_relation_data,exeBatch,rollback,get_vertex_data,get_edge_data,gen_edge_Batch,gen_vertex_Batch
from new import create_DB_space,create_TAG_RELATION,Delete_Space


# Main entry
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='load.py')
    parser.add_argument('--file',default='db.sqlite3',help='load DB file')
    parser.add_argument('--spacename',type=str,default="test",help='select nebula sapce')
    parser.add_argument('--project_id',default=6,help='the id for create the project examples')
    opt = parser.parse_args()
    relation,span = get_tag_relation_data(opt.file,opt.project_id)
    spacename = opt.spacename
    """
    config setting
    """
    # IP and port of the nebula-graphd service
    addr = "10.192.71.57"
    port = 9669
    # The default login
    usr = "root"
    pwd = "nebula"
    config = Config()
    config.max_connection_pool_size = 2
    # init connection pool
    connection_pool = ConnectionPool()
    
    # get session from the pool
    status = connection_pool.init([(addr, port)], config)
    client = connection_pool.get_session(usr, pwd)
    assert client is not None
    """
    create mode 
    """
    create_DB_space(client,spacename)
    create_TAG_RELATION(client,span,relation)
    time.sleep(20)
    """
    insert VERTEXT
    """
    i = 1
    while(True):
        vertex_example = get_vertex_data(opt.file,opt.project_id,i)
        edge_example = get_edge_data(opt.file,opt.project_id,i)
        #print(example)
        todo_vertex,undo_vertex = gen_vertex_Batch(vertex_example)
        todo_edge,undo_edge = gen_edge_Batch(edge_example)
        if not vertex_example:
            break
        else:
            i+=1
        if status:
            with connection_pool.session_context(usr, pwd) as session:
                progress_vertex = exeBatch(spacename, todo_vertex, session)
                if (progress_vertex != len(todo_vertex)):
                    if rollback(undo_vertex, progress_vertex, session) == False:
                        logging.error("Rollback failed.")
                    else:
                        logging.warning("Bacth insert failed, with all inserted vertices rolled back.")
                else:
                    logging.info("Vertex batch insert succeeded.")
                progress_edge = exeBatch(spacename, todo_edge, session)
                if (progress_edge != len(todo_edge)):
                    if rollback(undo_edge, progress_vertex, session) == False:
                        logging.error("Rollback failed.")
                    else:
                        logging.warning("Bacth insert failed, with all inserted edges rolled back.")
                else:
                    logging.info("Edge batch insert succeeded.")
        else:
            logging.error("Connection pool initialization failed.")
        connection_pool.close()
