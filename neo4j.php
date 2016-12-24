<?php
require_once 'vendor/autoload.php';

use GraphAware\Neo4j\Client\ClientBuilder;

$client = ClientBuilder::create()
        ->addConnection('bolt', 'bolt://neo4j:1232456@localhost:7687') // Example for HTTP connection configuration (port is optional)
        ->build();


function CreateNode(){
    // CREATE (node:Label1:Label2:Label3) case sensetive
    // so we can put alias on the labell
}


?>
