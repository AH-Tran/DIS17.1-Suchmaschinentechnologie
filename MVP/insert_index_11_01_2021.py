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

with open("synonyms_bearbeitet.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
for i in content:
    i.replace("_", " ")
#print(content)

#content =["coronavirus, sars-cov-2, sars-cov2, sars cov 2,covid19, covid-19, covid 19, covid" ] 
## index settings: mapping for publish_time
settings = {
    "settings": {
        # just one shard, no replicas for testing
        "number_of_shards": 1,
        "number_of_replicas": 0,

        # custom analyzer for covid metadata.csv
        "analysis": {
            "filter": {
                "synonym": {
                    "type": "synonym",
                    "lenient": True,
                    "synonyms": content
                },
                "my_snow":{
                    "type": "snowball",
                    "language": "English"}
            },
            "analyzer": {
                "covid_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "stopwords": "_english",
                    "filter": ["synonym",
                               "lowercase",
                               "stop",
                               "asciifolding",
                               "my_snow"]
                },
                "query_analyzer":{
                    "type": "custom",
                    "tokenizer": "standard",
                    "stopwords": "_english",
                    "filter": ["lowercase",
                               "stop",
                               "asciifolding",
                               "my_snow"]
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
            "query": {
                "type": "text",
                "analyzer": "query_analyzer"
            }
        }
    }
}

## Create Index
es.indices.create(index="covid_index", ignore=400, body=settings)
es.indices.analyze(index='covid_index', ignore=400, body=settings)

## Index Documents
# bulk(es, index="covid_index", doc_type="_doc", request_timeout=60, raise_on_error=False)
with open("metadata_update.csv", "r",
          encoding="utf8") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='covid_index', raise_on_error=False, stats_only=False)
