const fs = require('fs'),
      zlib = require('zlib'),
      readline = require('readline'),
      db = require('./neo4jDB'),
      KGItem = require('./KGItem');

const startImport = () => {
  const dumpPath = '/Users/yujunwu/Downloads/latest-all.json.gz',
        lineLimit = 100,
        start = new Date(),
        stream = fs.createReadStream(dumpPath).pipe(zlib.createGunzip());

  let lineCount = 0,
      itemCount = 0;

  stream.setEncoding('utf8');
  const lineReader = readline.createInterface({
          input: stream
        });

  lineReader.on('line', (data) => {
    data = data.replace(/,$/, '');

    if (data !== '[' && data !== ']') {
      lineCount += 1;
      try {
        KGItem.createFromWikiData(JSON.parse(data))
          .then(results => {
            itemCount += 1;
            console.log(`In ${parseInt((new Date() - start) / 1000)}s ${itemCount} main items saved.`);
          })
          .catch(err => {

          });
      } catch (err) {
        console.log('err:', err.stack || err);
        console.log('data:', data);
        lineReader.pause();
      } finally {
        if (lineCount >= lineLimit) {
          console.log(`In ${formattedTime(new Date(), start)} mins ${lineCount} read finishes.`);
          lineReader.pause();
        }
      }

      // KGItem.createFromWikiData(JSON.parse(data));
      // if (lineCount >= lineLimit) {
      //   lineReader.pause();
      // }
    }  
  });

  lineReader.on('close', () => {
    console.log(`In ${formattedTime(new Date(), start)} mins reading all data finishes.`);
  });

  // stream.on('data', (data) => {
  //   lineCount += 1;
  //   console.log('reading data...');
  //   // console.log('data:');
  //   console.log(data);

  //   if (lineCount >= lineLimit) {
  //     stream.pause();
  //   }
  // });

  stream.on('close', () => {
    console.log(`In ${formattedTime(new Date(), start)} mins reading all data finishes.`);
  });

  stream.on('error', err => {
    console.log(`In ${formattedTime(new Date(), start)} mins error occurs:`, err.stack || err);
  });
};

const formattedTime = (end, start) => {
  return ((end - start) / 1000 / 60).toFixed(1);
};

// return KGItem.deleteAll()
//   .then(results => {
//     console.log('All nodes deleted:', results);
//   })
//   .catch(err => console.log('err:', err.stack || err));

db.cypher({
  query: 'CREATE CONSTRAINT ON (item:Item) ASSERT item.item_id IS UNIQUE'
}, (err, results) => {
  if (err) return console.error('Create constraint on Item error:', err.stack || err);
  startImport();
});


