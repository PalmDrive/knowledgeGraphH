<?php
require __DIR__ . '/vendor/autoload.php';

include 'neo4j.php';

use Wikibase\JsonDumpReader\JsonDumpFactory;

$dumpPath = '/Users/yujunwu/Downloads/latest-all.json.gz';
$factory = new JsonDumpFactory();
$dumpReader = $factory->newGzDumpReader($dumpPath);

$t1 = time();

$dumpIterator = $factory->newStringDumpIterator( $dumpReader  );
foreach ( $dumpIterator as $jsonLine  ) {
    //$arr = json_decode($jsonLine);  
    //var_dump($arr); 
    echo 'reading...';
    // break;
}
$t2 = time();
echo 'Finished in '. (($t2 - $t1) / 60) .' mins.';
?>
