'use strict';

const readline = require('readline'),
      fs = require('fs'),
      csv = require('fast-csv');

const filePath = 'csv/items.csv';

let lineCount = 0;
const start = new Date();

try {
  const rs = fs.createReadStream(filePath);
  const csvStream = csv({headers: true})
    .on('data', data => {
      lineCount += 1;
      if (lineCount % 1000000 === 0) {
        console.log(`--- ${lineCount} lines scaned in ${parseInt((new Date() - start) / 1000)}s ---`);
      }
    })
    .on('end', () => {
      console.log(`--- ${lineCount} lines scan finished in ${parseInt((new Date() - start) / 1000)}s ---`);
    });

  rs.pipe(csvStream);
} catch (err) {
  console.log('Exception:', err.stack || err);
  console.log(`In line ${lineCount+1}`);
}
