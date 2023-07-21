"""
Template setting
"""
#查询实体相邻节点关系
entity_related_template = "MATCH (m)-[a]-(n) WHERE id(m)==\"%s\" OPTIONAL MATCH (n)-[b]-(l) RETURN id(m),tags(m),properties(m),src(a), dst(a), type(a),id(n),tags(n),properties(n),src(b), dst(b), type(b),id(l),tags(l),properties(l);"

#图空间语句
drop_space_template = "DROP SPACE IF EXISTS %s;"
create_space_template = "CREATE SPACE IF NOT EXISTS %s(vid_type=FIXED_STRING(256));"

#创建TAG、EDGE语句
load_TAG_template = "select * from label_types_relationtype where project_id = %d"
load_EDGE_template = "select * from label_types_spantype where project_id = %d"
create_TAG_template = "CREATE TAG IF NOT EXISTS `%s`(name string,ground_color string DEFAULT \"%s\",text_color string DEFAULT \"%s\");"
create_EDGE_template = "CREATE EDGE IF NOT EXISTS `%s`(rel_type int DEFAULT 0,name string DEFAULT \"%s\",ground_color string DEFAULT \"%s\",text_color string DEFAULT \"%s\");"

#查询所有实体语句
all_entities_template = "MATCH (v) RETURN v LIMIT %s,%s"

#查询实体点、边
vertex_data_template = " select start_offset,end_offset,l2.text,l3.text,l1.id from \
                  (select * from labels_span where example_id\
                  in (select  example_id from examples_examplestate where examples_examplestate.example_id \
                  in (select id from examples_example where project_id = %d) ) )  l1 \
                  left join label_types_spantype l2 on l1.label_id =  l2.id \
                  left join examples_example l3 on l1.example_id = l3.id\
                  limit %d,%d;"

edge_data_template = "select from_id_id,to_id_id,text from \
                  (select * from labels_relation where example_id\
                  in  (select  example_id from examples_examplestate where examples_examplestate.example_id\
                  in  (select id from examples_example where project_id =%d))) l1\
                  left join label_types_relationtype l2 on l1.type_id =  l2.id\
                  limit %d,%d;"

# Query template for todo queries
insert_Vertex_Template = "INSERT VERTEX `%s` (name) VALUES \"%s\":(\"%s\")"
# Query template for undo queries that delete the inserted vertices
rollback_Vertex_Template = "DELETE VERTEX \"%s\""

# Query template for todo queries
insert_EDGE_Template = "INSERT EDGE `%s` () VALUES \"%s\"->\"%s\":()"
# Query template for undo queries that delete the inserted vertices
rollback_EDGE_Template = "DELETE EDGE `%s` \"%s\"->\"%s\""