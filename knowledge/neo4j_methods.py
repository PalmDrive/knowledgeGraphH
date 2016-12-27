#coding=utf8

from neo4j.v1 import GraphDatabase, basic_auth

from knowledge.config.config import CONFIG

class Neo4jManager(object):
  def __init__(self):
    self.driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth(CONFIG.NEO4J_USERNAME, CONFIG.NEO4J_PASSWORD))
    self.session = self.driver.session()

  def close(self):
    self.session.close()

  # properties = {"name": value, key: value, ...}
  def create_entity(self, properties):

    clause = "MERGE (n {name: {name}"

    for key in properties:
      if key != "name":
        clause += ", %s: {%s}" % key

    clause += "}) RETURN n, n.name AS name"

    result = self.session.run(clause, properties)
    retained_result = list(result)

    return retained_result

  def create_edge(self, from_entity_name, to_entity_name, properties):
    clause = "MATCH (a),(b) WHERE a.name = '%s' AND b.name = '%s' CREATE (a)-[r:%s {name: {name}" % (from_entity_name, to_entity_name, properties['name'])

    for key in properties:
      if key != "name":
        clause += ", %s: {%s}" % key

    clause += "}]->(b) RETURN r, r.name AS name"

    result = self.session.run(clause, properties)
    retained_result = list(result)
    return retained_result

  def set_entity(self, entity_name, properties):
    clause = "MATCH (n { name: '%s' }) SET " % entity_name
    for key in properties:
      clause += "n.%s = '%s', " % (key, properties[key])

    clause = clause[:-2]
    clause += " RETURN n, n.name AS name"

    result = self.session.run(clause)
    retained_result = list(result)
    return retained_result

  def set_edge(self, edge_name, properties):
    clause = "MATCH (sub)-[r:%s]->(obj) SET " % edge_name
    for key in properties:
      clause += "r.%s = '%s', " % (key, properties[key])

    clause = clause[:-2]
    clause += " RETURN r, r.name AS name"

    result = self.session.run(clause)
    retained_result = list(result)
    return retained_result

  def find_edges(self, edge_name, from_entity_name=None, to_entity_name=None, **kwargs):
    clause = "MATCH (sub"

    if from_entity_name:
      clause += " { name: '%s'})-[r:%s" % (from_entity_name, edge_name)
    else:
      clause += ")-[r:%s" % edge_name

    condition = ""
    if kwargs:
      for key in kwargs:
        if kwargs[key]:
          condition += "%s: '%s', " % (key, kwargs[key])

    if len(condition) > 0:
      condition = condition[:-2]
      clause += "{ " + condition + " }]->(obj"
    else:
      clause += "]->(obj"

    if to_entity_name:
      clause += " { name: '%s'})" % to_entity_name
    else:
      clause += ")"

    clause += "RETURN r.name AS edge_name, r.IO AS IO, sub.name AS from_name, obj.name AS to_name"

    print 'clause : ' + clause
    result = self.session.run(clause)
    retained_result = list(result)
    return retained_result

  def find_from_entity(self, edge):
    name = edge['name']

    clause = "MATCH (sub)-[r:%s]->(obj) RETURN sub AS entity, sub.name AS name" % name

    result = self.session.run(clause)
    retained_result = list(result)
    return retained_result

  def find_to_entity(self, edge):
    name = edge['name']

    clause = "MATCH (sub)-[r:%s]->(obj) RETURN obj AS entity, obj.name AS name" % name

    print 'clause : ' + clause
    result = self.session.run(clause)
    retained_result = list(result)
    return retained_result

  def find_nodes_with_labels(self, labels):
    label_query = ""
    for label in labels:
      label_query += (":" + label)
    clause = "MATCH (n%s) RETURN n, labels(n) AS labels" % label_query
    result = self.session.run(clause)
    retained_result = list([(r['n'], r['labels']) for r in result])
    return retained_result

  def find_nodes_with_any_values_in_properties(self, **kwargs):
    predicates = []
    for property in kwargs:
      predicates.append("'"+ kwargs[property] +"' in n." + property)
    predicate = ' OR '.join(predicates)
    clause = "MATCH (n) WHERE %s RETURN n" % predicate

    result = self.session.run(clause)
    retained_result = list([r['n'] for r in result])
    return retained_result

if __name__ == '__main__':
    db = GraphDatabase()
    print(db.find_to_entity({'name': u'送'}))
