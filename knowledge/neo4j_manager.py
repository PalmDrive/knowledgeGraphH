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

    query = "MERGE (n {name: {name}"

    for key in properties:
      if key != "name":
        query += ", %s: {%s}" % key

    query += "}) RETURN n, n.name AS name"

    result = self.session.run(query, properties)
    retained_result = list(result)

    return retained_result

  def create_edge(self, from_entity_name, to_entity_name, properties):
    query = "MATCH (a),(b) WHERE a.name = '%s' AND b.name = '%s' CREATE (a)-[r:%s {name: {name}" % (from_entity_name, to_entity_name, properties['name'])

    for key in properties:
      if key != "name":
        query += ", %s: {%s}" % key

    query += "}]->(b) RETURN r, r.name AS name"

    result = self.session.run(query, properties)
    retained_result = list(result)
    return retained_result

  def set_entity(self, entity_name, properties):
    query = "MATCH (n { name: '%s' }) SET " % entity_name
    for key in properties:
      query += "n.%s = '%s', " % (key, properties[key])

    query = query[:-2]
    query += " RETURN n, n.name AS name"

    result = self.session.run(query)
    retained_result = list(result)
    return retained_result

  def set_edge(self, edge_name, properties):
    query = "MATCH (sub)-[r:%s]->(obj) SET " % edge_name
    for key in properties:
      query += "r.%s = '%s', " % (key, properties[key])

    query = query[:-2]
    query += " RETURN r, r.name AS name"

    result = self.session.run(query)
    retained_result = list(result)
    return retained_result

  def find_edges(self, edge_name, from_entity_name=None, to_entity_name=None, **kwargs):
    query = "MATCH (sub"

    if from_entity_name:
      query += " { name: '%s'})-[r:%s" % (from_entity_name, edge_name)
    else:
      query += ")-[r:%s" % edge_name

    condition = ""
    if kwargs:
      for key in kwargs:
        if kwargs[key]:
          condition += "%s: '%s', " % (key, kwargs[key])

    if len(condition) > 0:
      condition = condition[:-2]
      query += "{ " + condition + " }]->(obj"
    else:
      query += "]->(obj"

    if to_entity_name:
      query += " { name: '%s'})" % to_entity_name
    else:
      query += ")"

    query += "RETURN r.name AS edge_name, r.IO AS IO, sub.name AS from_name, obj.name AS to_name"

    print 'query : ' + query
    result = self.session.run(query)
    retained_result = list(result)
    return retained_result

  def find_from_entity(self, edge):
    name = edge['name']

    query = "MATCH (sub)-[r:%s]->(obj) RETURN sub AS entity, sub.name AS name" % name

    result = self.session.run(query)
    retained_result = list(result)
    return retained_result

  def find_to_entity(self, edge):
    name = edge['name']

    query = "MATCH (sub)-[r:%s]->(obj) RETURN obj AS entity, obj.name AS name" % name

    print 'query : ' + query
    result = self.session.run(query)
    retained_result = list(result)
    return retained_result

  def find_nodes_with_labels(self, labels):
    label_query = ""
    for label in labels:
      label_query += (":" + label)
    query = "MATCH (n%s) RETURN n, labels(n) AS labels" % label_query
    result = self.session.run(query)
    retained_result = list([(r['n'], r['labels']) for r in result])
    return retained_result

  def find_nodes_with_any_values_in_properties(self, **kwargs):
    predicates = []
    for property in kwargs:
      predicates.append("'"+ kwargs[property] +"' in n." + property)
    predicate = ' OR '.join(predicates)
    query = "MATCH (n) WHERE %s RETURN n" % predicate

    result = self.session.run(query)
    retained_result = list([r['n'] for r in result])
    return retained_result

  def find_neighbor_nodes(self, entity_id, max_distance):
    query = "MATCH path = (n)-[*0..%d]-(m) WHERE n.item_id = '%s' RETURN m, length(path) AS distance" \
            % (max_distance, entity_id)

    result = self.session.run(query)
    retained_result = list([(r['m'], r['distance']) for r in result])
    return retained_result

if __name__ == '__main__':
    db = Neo4jManager()
    print(db.find_to_entity({'name': u'送'}))
