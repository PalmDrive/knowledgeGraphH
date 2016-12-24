<?php
require __DIR__ . '/vendor/autoload.php';

include 'neo4j.php';

use Wikibase\JsonDumpReader\JsonDumpFactory;

$factory = new JsonDumpFactory();
$dumpReader = $factory->newGzDumpReader( 'latest-all.json.gz'  );

$dumpIterator = $factory->newStringDumpIterator( $dumpReader  );
foreach ( $dumpIterator as $jsonLine  ) {
    $arr = json_decode($jsonLine);  
    var_dump($arr); 

    break;
}
?>
