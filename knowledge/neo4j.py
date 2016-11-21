#coding=utf8

from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "junlinguzhong"))

# properties = {"name": value, key: value, ...}
def create_entity(properties):
  session = driver.session()
  clause = "CREATE (n {name: {name}"

  for key, value in properties:
    if key != "name":
      clause += ", %s: {%s}" % key
  
  clause += "}) RETURN n"
  
  result = session.run(clause, properties)
  retained_result = list(result)
  session.close()
  return retained_result

def create_edge(from_node, to_node, properties):
  session = driver.session()
  clause = "MATCH (a),(b) WHERE a.name = '%s' AND b.name = '%s' CREATE (a)-[r:{name} {name: {name}" % (from_node, to_node)

  for key, value in properties:
    if key != "name":
      clause += ", %s: {%s}" % key

  clause += "}]->(b) RETURN r"
  
  result = session.run(clause, properties)
  retained_result = list(result)
  session.close()
  return retained_result

def set_entity(entity_name, properties):
  session = driver.session()
  clause = "MATCH (n { name: '%s' }) SET " % entity_name
  for key, value in properties:
    clause += "n.%s = {%s}, " % key

  clause = clause[:-2]
  clause += " RETURN n"

  result = session.run(clause, properties)
  retained_result = list(result)
  session.close()
  return retained_result

def set_edge(edge_name, properties):
  session = driver.session()
  clause = "MATCH (sub)-[r:{name}]->(obj) SET " % edge_name
  for key, value in properties:
    clause += "n.%s = {%s}, " % key

  clause = clause[:-2]
  clause += " RETURN r"

  result = session.run(clause, properties)
  retained_result = list(result)
  session.close()
  return retained_result

def find_edges(edge_name, from_entity_name=None, to_entity_name=None, **kwargs):
  session = driver.session()
  clause = "MATCH (sub"

  if from_entity_name:
    clause += " { name: '%s'})-[r:'%s'" % (from_entity_name, edge_name)
  else:
    clause += ")-[r:'%s'" % edge_name

  clause += "{ "

  for key, value in kwargs:
    clause += "%s: '%s', " % (key, value)

  clause = clause[:-2]
  clause += " }]->(obj"

  if to_entity_name:
    clause += " { name: '%s'}) RETURN r, r.name AS name" % to_entity_name
  else:
    clause += ") RETURN r, r.name AS name"

  result = session.run(clause)
  retained_result = list(result)
  return retained_result

def find_from_entity(edge):
  name = edge.name
  clause = "MATCH (sub)-[r:'%s']->(obj) RETURN sub AS entity, sub.name AS name" % name
  
  session = driver.session()
  result = session.run(clause)
  retained_result = list(result)
  return retained_result

def find_to_entity(edge):
  name = edge.name
  clause = "MATCH (sub)-[r:'%s']->(obj) RETURN obj AS entity, obj.name AS name" % name
  
  session = driver.session()
  result = session.run(clause)
  retained_result = list(result)
  return retained_result

if __name__ == '__main__':
    create_entity({name: "花"})
