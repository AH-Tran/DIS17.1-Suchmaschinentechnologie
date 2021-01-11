from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from datetime import datetime
import os, uuid
import pandas as pd
import csv, itertools, json
import requests

## Connect to Elasticsearch
es = Elasticsearch([{"host": "localhost", "port": 9200}])
index_name= "test2"

## Check if Index already exists
if es.indices.exists(index_name):
    es.indices.delete(index=index_name)

## Index Settings
doc_settings={
    "settings": {
    # just one shard, no replicas for testing
        "number_of_shards": 1,
        "number_of_replicas": 0,
 #ANALYSIS
        "analysis": {
        #FILTER
            "filter": { 
              #KEYWORD
              "keyword_list": {
                "type": "keyword_marker",# plural or singular?
                "keywords": ["Covid-19", "SARS-COV-2", "SARS-COV", "2019-nCOV"
                         "United States", "United Kingdom", "Hong Kong", "United Arab Emirates",
                         "non-social", "African-American",
                          "mRNA ", "ACE inhibitor", "enzyme inhibitors", "blood type", "Angiotensin-converting", "clinical signs", "super spreaders", "hand sanitizer", "alcohol sanitizer", ""]#
                 },
                #nGRAM
                "tokenizer": {
                "ngram_tokenizer": {
                    "type": "ngram",
                    "min_gram": 3,
                    "max_gram": 3,
                    "token_chars": [
                        "letter",
                        "digit",
                        "punctuation",
                        "symbol"
                    ]
                  }
                  },
                 #STEM
                "english_stemmer" : {
                    "type" : "stemmer",
                    "name" : "english"
                },
                                #CHAR FILTER
                "char_filter": {
                    "substitute": {
                      "type": "mapping",
                      "mappings": [
                        "$=> dollar",
                        "€=> euro",
                        "£=> pound",
                        "%=> percentage"
                        ]
                    },
                }
                },
                #SIMILARITY
                "index": {
                "similarity": {
                  "short_similarity": {
                    "type": "BM25",
                    "k1": "1.2", #the higher, the more relevant TF
                    "b": "0.75" #the higher, the higher the impact of document length
                  },
                  "long_similarity": {
                    "type": "DFR",
                    "basic_model": "g",
                    "after_effect": "l",
                    "normalization": "h2"
                  }
                }
    },
        #CUSTOM ANALYZER
            "analyzer": {
            "covid_analyzer": {
              "type": "custom",
              "tokenizer": "standard",
              "stopwords": "_english",
              "filter": ["lowercase",
                        "stop",
                        "asciifolding",
                        "english_stemmer",
                        "keyword_list",
                        "char_filter"
                        ]  
            },
             "ngram_analyzer": {
              "tokenizer": "ngram_tokenizer",
            }
          }# analyzer end
        }# analysis end
    },# settings end
##MAPPINGS
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "covid_analyzer",
                "similarity": "short_similarity",
                "fields": {
                  "ngram": {
                    "type": "string",
                    "analyzer": "ngram_analyzer"
                  }
                }
            },
            "abstract": {
                "type": "text",
                "analyzer": "covid_analyzer",
            "similarity": "long_similarity"
            },
            "publish_time": {
                "type": "date"
            }
        }
    }
}

## Create Index
es.indices.create(index=index_name , ignore=400, body=doc_settings)
#es.indices.analyze(index=index_name, ignore=400, body=doc_settings)

## Index Documents
with open("./MVP/metadata.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index=index_name,raise_on_error=False, stats_only=False)