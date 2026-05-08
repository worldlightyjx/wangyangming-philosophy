const fs = require('fs');

// Read source
const sourceContent = fs.readFileSync('data/volumes/juan02-cxl-zhong.js', 'utf8');
const sourceMatch = sourceContent.match(/window\.BOOK_VOLUMES\["juan02-cxl-zhong"\] = ({.*});/s);
const sourceData = JSON.parse(sourceMatch[1]);

// Extract blocks 35-69
const blocks = [];
for (let i = 35; i <= 69; i++) {
  const block = sourceData.blocks[i];
  blocks.push({
    idx: i,
    type: block.type,
    wen: block.wen || '',
    title: block.title || ''
  });
}

console.log(JSON.stringify(blocks, null, 2));
