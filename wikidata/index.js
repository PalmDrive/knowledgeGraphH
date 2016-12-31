const fs = require('fs'),
      zlib = require('zlib'),
      readline = require('readline'),
      db = require('./neo4jDB'),
      KGItem = require('./KGItem');

const startImport = () => {
  const dumpPath = '/Users/yujunwu/Downloads/latest-all.json.gz',
        lineBatch = 2500,
        lineLimit = Infinity,// 20000,
        start = new Date(),
        stream = fs.createReadStream(dumpPath).pipe(zlib.createGunzip());

  let lineCount = 0,
      itemCount = 0,
      cachedData = [],
      hasHeader = true;

  stream.setEncoding('utf8');
  const lineReader = readline.createInterface({
          input: stream
        });

  lineReader.on('line', (data) => {
    data = data.replace(/,$/, '');

    if (data !== '[' && data !== ']') {
      lineCount += 1;
      try {
        cachedData.push(JSON.parse(data));

        if (lineCount > lineLimit) {
          return lineReader.close();
        }

        if (lineCount % lineBatch === 0) {
          lineReader.pause();
          KGItem.write2csv(cachedData, {
            hasCSVColumnTitle: hasHeader
          })
            .then(res => {
              console.log(`In ${parseInt((new Date() - start) / 1000)}s ${res[0].length} nodes saved.`);
              itemCount += res[0].length;

              cachedData = [];
              hasHeader = false;
              lineReader.resume();
            })
            .catch(err => console.log('err:', err.stack || err));
        }

        // KGItem.createFromWikiData(JSON.parse(data))
        //   .then(results => {
        //     itemCount += 1;
        //     console.log(`In ${parseInt((new Date() - start) / 1000)}s ${itemCount} main items saved.`);
        //   })
        //   .catch(err => {

        //   });
      } catch (err) {
        console.log('catch exception:', err.stack || err);
        console.log('data:', data);
        lineReader.pause();
      }

      // KGItem.createFromWikiData(JSON.parse(data));
      // if (lineCount >= lineLimit) {
      //   lineReader.pause();
      // }
    }  
  });

  lineReader.on('close', () => {
    if (cachedData.length) {
      console.log(`Process the last ${cachedData.length} data...`);
      KGItem.write2csv(cachedData, {
        hasCSVColumnTitle: hasHeader
      })
        .then(res => {
          cachedData = [];
          console.log(`In ${parseInt((new Date() - start) / 1000)}s ${res[0].length} nodes saved.`);
          itemCount += res[0].length;
          console.log(`In ${formattedTime(new Date(), start)} mins reading all ${lineCount} lines finishes.`);
        })
        .catch(err => console.log('err:', err.stack || err));
    } else {
      console.log(`In ${formattedTime(new Date(), start)} mins reading all ${lineCount} finishes.`);
    }
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

  // stream.on('end', () => {
  //   console.log(`In ${formattedTime(new Date(), start)} mins reading all data finishes.`);
  // });

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

// db.cypher({
//   query: 'CREATE CONSTRAINT ON (item:Item) ASSERT item.item_id IS UNIQUE'
// }, (err, results) => {
//   if (err) return console.error('Create constraint on Item error:', err.stack || err);
//   startImport();
// });
startImport();


