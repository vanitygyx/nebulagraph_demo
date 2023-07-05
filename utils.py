import sqlite3
import logging

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
        cur.execute("select * from label_types_relationtype where project_id = %d"%(project_id))
        relationtype_all = cur.fetchall() 
        cur.execute("select * from label_types_spantype where project_id = %d"%(project_id))
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
      cur.execute(" select start_offset,end_offset,l2.text,l3.text from \
                  (select * from labels_span where example_id\
                  in (select  example_id from examples_examplestate where examples_examplestate.example_id \
                  in (select id from examples_example where project_id = %d) ) )  l1 \
                  left join label_types_spantype l2 on l1.label_id =  l2.id \
                  left join examples_example l3 on l1.example_id = l3.id\
                  limit %d,%d;"%(project_id,(num-1)*500,num*500))
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
      cur.execute(" select l2.start_offset,l2.end_offset,l3.start_offset,l3.end_offset,l4.text,l5.text from \
                  (select * from labels_relation where example_id\
                  in  (select  example_id from examples_examplestate where examples_examplestate.example_id\
                  in  (select id from examples_example where project_id =%d))) l1\
                  left join labels_span l2 on l1.from_id_id = l2.id\
                  left join labels_span l3 on l1.to_id_id = l3.id\
                  left join examples_example l4 on l1.example_id = l4.id\
                  left join label_types_relationtype l5 on l1.type_id =  l5.id\
                  limit %d,%d;"%(project_id,(num-1)*500,num*500))
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
  # Query template for todo queries
  insertVertexTemplate = "INSERT VERTEX `%s` (name) VALUES \"%s\":(\"%s\")"
  # Query template for undo queries that delete the inserted vertices
  rollbackTemplate = "DELETE VERTEX \"%s\""
  todo = []
  undo = []
  for table in data:
    start,end = table[0],table[1]
    value = table[3][start:end]
    #print(value)
    value =value.replace('"',"\\\"")
    insert = insertVertexTemplate % (table[2],value,value)
    rollback = rollbackTemplate % (value)
    todo.append(insert)
    undo.append(rollback)
  # Ingest some errors for testing:
  # undo[0] = insertVertexTemplate
  # todo[4] = insertVertexTemplate
  return todo, undo

def gen_edge_Batch(data):
  # Query template for todo queries
  insertVertexTemplate = "INSERT EDGE `%s` () VALUES \"%s\"->\"%s\":()"
  # Query template for undo queries that delete the inserted vertices
  rollbackTemplate = "DELETE EDGE `%s` \"%s\"->\"%s\""
  todo = []
  undo = []
  for table in data:
    start1,end1 = table[0],table[1]
    start2,end2 = table[2],table[3]
    src = table[4][start1:end1]
    dst = table[4][start2:end2]
    src =src.replace('"',"\\\"")
    dst =dst.replace('"',"\\\"")
    #print(src,dst)
    insert = insertVertexTemplate % (table[5],src,dst)
    rollback = rollbackTemplate % (table[5],src,dst)
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
  if i == retryTimes:
    logging.error("Error %s (%d), while executing query %s." % (result.error_msg(), result.error_code(), query))
    return None
  elif result.is_succeeded():
    return result
  else:
    raise Exception("Failed at trying to execute query %s." % (query))
  
