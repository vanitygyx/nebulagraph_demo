import argparse
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
import config as cf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='scan_vertext_relation.py')
    parser.add_argument('--spacename',type=str,default="test",help='select nebula sapce')
    parser.add_argument('--scan_id',type=str,default="ion\" conte",help='the id for scaning vertexs and edges')

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
    result = client.execute("MATCH (m)-[a]->(n) WHERE id(m)==\"%s\" OPTIONAL MATCH (n)-[b]->(l) RETURN m,a,n,b,l;"%(opt.scan_id))
    print(result)
    connection_pool.close()