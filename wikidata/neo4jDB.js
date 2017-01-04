'use strict';

const neo4j = require('neo4j');

const dbConfig = {
  username: 'neo4j',
  password: 'neo4j2016',
  url: 'http://localhost:7474'
},
db = new neo4j.GraphDatabase({
  url: dbConfig.url,
  auth: {username: dbConfig.username, password: dbConfig.password}
});

module.exports = db;