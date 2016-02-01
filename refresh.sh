#!/bin/bash
INDEX="familiasskus"
curl -XDELETE 10.151.1.21:9200/$INDEX/?pretty
curl -XPUT 10.151.1.21:9200/$INDEX/?pretty
curl -XPUT 10.151.1.21:9200/$INDEX/_mapping/$INDEX?pretty --data-binary @mapping.json

INDEX="skuhier"
curl -XDELETE 10.151.1.21:9200/$INDEX/?pretty
curl -XPUT 10.151.1.21:9200/$INDEX/?pretty
