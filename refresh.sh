#!/bin/bash
curl -XDELETE 10.151.1.21:9200/skuhier/?pretty
curl -XPUT 10.151.1.21:9200/skuhier/?pretty
#curl -XPUT 10.151.1.21:9200/ventas/_mapping/venta?pretty --data-binary @venda/mapping.json

