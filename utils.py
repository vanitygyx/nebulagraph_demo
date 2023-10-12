import sqlite3
import logging
import template as temp
# Retry each query execution for the following times
retryTimes = 10

def get_tag_relation_data(filename,project_id):
    relationtype_all = []
    spantype_all = []
    examples_all = []
    con = sqlite3.connect(filename) 
    cur = con.cursor() 
    try: 
    # 获取所有数据 
        cur.execute(temp.load_TAG_template%(project_id))
        relationtype_all = cur.fetchall() 
        cur.execute(temp.load_EDGE_template%(project_id))
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

def get_vertex_data(filename,project_id=1,num=1):
  con = sqlite3.connect(filename) 
  cur = con.cursor() 
  examples_all = []
  try:
      cur.execute(temp.vertex_data_template%(project_id,(num-1)*500,num*500))
      examples_all = cur.fetchall()
  except Exception as e: 
    print(e) 
    print('查询失败')   
  return examples_all

def get_edge_data(filename,project_id=1,num=1):
  con = sqlite3.connect(filename) 
  cur = con.cursor() 
  examples_all = []
  try:
      cur.execute(temp.edge_data_template%(project_id,(num-1)*500,num*500))
      examples_all = cur.fetchall()
  except Exception as e: 
    print(e) 
    print('查询失败')   
  return examples_all

# Execute queries in a batch.
def exeBatch(space, batch, session):
  counter = 0
  session.execute("use " + space)
  for query in batch:
    result = exeQueryWithRetries(query, session)
    if result == None:
      return counter
    else:
      counter = counter + 1
  return counter

def gen_vertex_Batch(data):

  todo = []
  undo = []
  for table in data:
    start,end = table[0],table[1]
    value = table[3][start:end]
    #print(value)
    value =value.replace('"',"\\\"")
    value =value.replace("\n","")
    insert = temp.insert_Vertex_Template % (table[2],table[4],value)
    rollback = temp.rollback_Vertex_Template % (table[4])
    todo.append(insert)
    undo.append(rollback)
  # Ingest some errors for testing:
  # undo[0] = insertVertexTemplate
  # todo[4] = insertVertexTemplate
  return todo, undo

def gen_edge_Batch(data):

  todo = []
  undo = []
  for table in data:
    #print(src,dst)
    insert = temp.insert_EDGE_Template % (table[2],table[0],table[1])
    rollback = temp.rollback_EDGE_Template % (table[2],table[0],table[1])
    todo.append(insert)
    undo.append(rollback)
  return todo, undo

# Rollback the batch execution by executing the undo counterparts of all successfully executed queries.
def rollback(undo, progress, session):
  count = 0
  while (count < progress):
    result = exeQueryWithRetries(undo[count], session)
    if result == None:
      logging.error("Rollback failed while executing the %d-th undo statement \"%s\"." % (count, undo[count]))
      return False
    else:
      count = count + 1
  if count == progress:
    return True
  else:
    return False
  
def exeQueryWithRetries(query, session):
  result = session.execute(query)
  if result.is_succeeded():
    return result
  i = 0
  while i < retryTimes:
    logging.info("Executing %s." % query)
    result = session.execute(query)
    if not result.is_succeeded():
      i = i + 1
    else:
      break
  if i == retryTimes :
    try:
      logging.error("Error %s (%d), while executing query %s." % (result.error_msg(), result.error_code(), query))
    finally:
      print(query)
      return None
  elif result.is_succeeded():
    return result
  else:
    raise Exception("Failed at trying to execute query %s." % (query))
  
