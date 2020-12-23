from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from datetime import datetime
import os, uuid
import pandas as pd
import csv, itertools, json
import requests

## Connect to Elasticsearch
es = Elasticsearch([{"host": "localhost", "port": 9200}])

## Check if Index already exists
if es.indices.exists("covid_index"):
    es.indices.delete(index="covid_index")

## index settings: mapping for publish_time
settings={
    "settings": {
        # just one shard, no replicas for testing
        "number_of_shards": 1,
        "number_of_replicas": 0,

        # custom analyzer for covid metadata.csv
        "analysis": {
          "analyzer": {
            "covid_analyzer": {
              "type": "custom",
              "tokenizer": "standard",
              "stopwords": "_english",
              "filter": ["lowercase",
                        "stop",
                        "asciifolding"
              ]  
            }
          }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "covid_analyzer"
            },
            "abstract": {
                "type": "text",
                "analyzer": "covid_analyzer"
            },
            "publish_time": {
                "type": "date"
            },
            "query" :  {
            "type": "text",
            "analyzer":"covid_analyzer"
            }
        }
    }
}

## Create Index
es.indices.create(index="covid_index", ignore=400, body=settings)
es.indices.analyze(index='covid_index', ignore=400, body=settings)

## Index Documents
#bulk(es, index="covid_index", doc_type="_doc", request_timeout=60, raise_on_error=False)
with open("C:/Users/Andreas/Documents/Studium/DIS17.1 Suchmaschinentechnologien/Projekt/metadata.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='covid_index',raise_on_error=False, stats_only=False)