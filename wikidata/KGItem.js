'use strict';
 
const _ = require('underscore'),
    objectPath = require('object-path'),
    db = require('./neo4jDB'),
    json2csv = require('json2csv'),
    fs = require('fs');

class KGItem {
  constructor(data) {
    
  }

  static _getItemIdFromClaim(claim) {
    return 'Q' + objectPath.get(claim, 'mainsnak.datavalue.value.numeric-id');
  }
  
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
  static _getLinkedNode(claimsDict, itemId) {
    return _.reduce(claimsDict, (memo, claims, pId) => {
      const items = claims.filter(claim => objectPath.get(claim, 'mainsnak.datatype') === 'wikibase-item' && KGItem._getItemIdFromClaim(claim) !== itemId)
        .map(claim => {
          return {
            relationship: {
              rel_type: pId,
              property_id: pId
            },
            item: {
              item_id: KGItem._getItemIdFromClaim(claim)
            }
          };
        });
      memo = memo.concat(items);
      return memo;
    }, []);
  }

  static _getRels(claimsDict, itemId) {
    return _.reduce(claimsDict, (memo, claims, pId) => {
      const filteredClaims = claims.filter(claim => objectPath.get(claim, 'mainsnak.datatype') === 'wikibase-item' && KGItem._getItemIdFromClaim(claim) !== itemId);
      memo = memo.concat(filteredClaims.map(claim => {
        const linkedItemId = KGItem._getItemIdFromClaim(claim);
        return {
          ':START_ID': itemId,
          ':END_ID': linkedItemId,
          ':TYPE': pId,
          property_id: pId
        };
      }));
      return memo;
    }, []);
  }

  static _getMainNode(data) {
    const getAliases = (lan) => {
      const aliases = objectPath.get('data', 'aliases.zh');
      if (aliases && aliases.length) {
        return aliases.map(obj => obj.value);
      } else {
        return undefined;
      }
    };

    const json = {
      item_id: data.id,
      label_zh: objectPath.get(data, 'labels.zh.value'),
      label_en: objectPath.get(data, 'labels.en.value'),
      aliases_zh: getAliases('zh'),
      aliases_en: getAliases('en'),
      description_zh: objectPath.get(data, 'descriptions.zh.value'),
      description_en: objectPath.get(data, 'descriptions.en.value')
    };
    return json;
  }

  static write2csv(data) {
    const nodeFilePath = 'csv/items.csv',
          relsFilePath = 'csv/rels.csv',
          nodeFields = [
            {
              label: 'item_id:ID',
              value: 'item_id'
            }, {
              label: 'label_zh', 
              value: 'label_zh'
            },
            {
              label: 'label_en', 
              value: 'label_en'
            },
            {
              label: 'description_en', 
              value: 'description_en'
            },
            {
              label: 'description_zh',
              value: 'description_zh'
            },
            {
              label: 'aliases_en:string[]', 
              value: 'aliases_en'
            },
            {
              lbel: 'aliases_zh:string[]',
              value: 'aliases_en'
            }
          ],
          relFields = [':START_ID', ':END_ID', ':TYPE', 'property_id'],
          nodesJson = data.map(d => KGItem._getMainNode(d)),
          relsJson = data.reduce((memo, d) => {
            memo = memo.concat(KGItem._getRels(d.claims || {}, d.id));
            return memo;
          }, []);

    const _write2csv = (filePath, data, fields) => {
      return new Promise((resolve, reject) => {
        fs.appendFile(filePath, json2csv({
          data,
          fields
        }), err => {
          if (err) return reject(err);
          resolve(data);
        });
      })
    };

    return Promise.all([
      _write2csv(nodeFilePath, nodesJson, nodeFields),
      _write2csv(relsFilePath, relsJson, relFields)
    ]);
  }

  static createFromWikiData(data, cb) {
    const setAttributes = (json) => {
      const res = [];
      for (let key in json) {
        if (key !== 'item_id' && json[key]) {
          res.push(`item.${key} = {${key}}`);
        }
      }
      return res.join(',');
    };

    const json = KGItem._getMainNode(data),
      linkedItems = KGItem._getLinkedItems(data.claims || {}, json.item_id);

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