import argparse
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
from nebula3.common import *
import logging
import time
from utils import get_tag_relation_data,exeBatch,rollback,get_vertex_data,genBatch
from new import create_DB_space,create_TAG_RELATION


# Main entry
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='create_demo.py')
    parser.add_argument('--file',default='db.sqlite3',help='load DB file')
    parser.add_argument('--spacename',type=str,default="test",help='select nebula sapce')
    parser.add_argument('--project_id',default=12,help='the id for create the project examples')
    opt = parser.parse_args()
    relation,span = get_tag_relation_data(opt.file)
    spacename = opt.spacename
    """
    config setting
    """
    # IP and port of the nebula-graphd service
    addr = "192.168.1.7"
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
        example = get_vertex_data(opt.file,opt.project_id,i)
        #print(example)
        todo,undo = genBatch(example)
        if not example:
            break
        else:
            i+=1
        if status:
            with connection_pool.session_context(usr, pwd) as session:
                progress = exeBatch(spacename, todo, session)
                if (progress != len(todo)):
                    if rollback(undo, progress, session) == False:
                        logging.error("Rollback failed.")
                    else:
                        logging.warning("Bacth insert failed, with all inserted vertices rolled back.")
                else:
                    logging.info("Batch insert succeeded.")
        else:
            logging.error("Connection pool initialization failed.")
        connection_pool.close()
