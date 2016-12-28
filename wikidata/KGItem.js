'use strict';
 
const _ = require('underscore'),
    objectPath = require('object-path'),
    db = require('./neo4jDB');

class KGItem {
  constructor(data) {
    Object.assign(this, data);
  }

  static createFromWikiData(data, cb) {
    const getAliases = (lan) => {
      const aliases = objectPath.get('data', 'aliases.zh');
      if (aliases && aliases.length) {
        return aliases.map(obj => obj.value);
      } else {
        return undefined;
      }
    };

    const setAttributes = (json) => {
      const res = [];
      for (let key in json) {
        if (key !== 'item_id' && json[key]) {
          res.push(`item.${key} = {${key}}`);
        }
      }
      return res.join(',');
    };
    
    /**
     * [description]
     * @param  {Dict} claims [description]
     * @return {Array}        [description]
     * [
     *   {
     *     relationship: {
     *       rel_type[string],
     *       property_id[string]
     *     }
     *     item: {item_id[string]}
     *   }
     * ]
     */
    const getLinkedItems = (claimsDict, itemId) => {
      const getItemId = (claim) => {
        return 'Q' + objectPath.get(claim, 'mainsnak.datavalue.value.numeric-id');
      };

      return _.reduce(claimsDict, (memo, claims, pId) => {
        const items = claims.filter(claim => objectPath.get(claim, 'mainsnak.datatype') === 'wikibase-item' && getItemId(claim) !== itemId)
          .map(claim => {
            return {
              relationship: {
                rel_type: pId,
                property_id: pId
              },
              item: {
                item_id: getItemId(claim)
              }
            };
          });
        memo = memo.concat(items);
        return memo;
      }, []);
    };

    const json = {
      item_id: data.id,
      label_zh: objectPath.get(data, 'labels.zh.value'),
      label_en: objectPath.get(data, 'labels.en.value'),
      aliases_zh: getAliases('zh'),
      aliases_en: getAliases('en'),
      description_zh: objectPath.get(data, 'descriptions.zh.value'),
      description_en: objectPath.get(data, 'descriptions.en.value')
    },
      linkedItems = getLinkedItems(data.claims || {}, json.item_id);

    let query = `
      MERGE (item:Item {item_id: {item_id}}) 
      ON CREATE SET ${setAttributes(json)} 
      ON MATCH SET ${setAttributes(json)}
    `;
    if (linkedItems.length) {
      const linkedItemsQuery = linkedItems.map((item, index) => {
        return `
          MERGE (linkedItem${index}:Item {item_id: '${item.item.item_id}'})
          MERGE (item)-[:${item.relationship.rel_type} {property_id: '${item.relationship.property_id}'}]->(linkedItem${index})
        `;
      }).join(' ');

      query += ' ' + linkedItemsQuery + ' RETURN item';
    }

    // console.log('query:', query);
    // console.log('params:', json);

    return new Promise((resolve, reject) => {
      db.cypher({
        query,
        params: json
      }, (err, results) => {
        if (err) {
          return console.log('Create item error:', err.stack || err);
          reject(err);
        }
        console.log('results:', results);
        resolve(results);
      });
    });
  }

  static deleteAll() {
    return new Promise((resolve, reject) => {
      db.cypher({
        query: 'MATCH (item) DETACH DELETE item'
      }, (err, results) => {
        if (err) return reject(err);
        resolve(results);
      });
    });
  }
};

module.exports = KGItem;