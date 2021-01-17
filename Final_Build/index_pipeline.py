from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from datetime import datetime
import os, uuid
import pandas as pd
import csv, itertools, json
import requests

## Connect to Elasticsearch
es = Elasticsearch([{"host": "localhost", "port": 9200}])
index_name= "covid_index2"
## Check if Index already exists
if es.indices.exists(index_name):
    es.indices.delete(index=index_name)

with open("./Final_Build/synonyms_bearbeitet.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
for i in content:
    i.replace("_", " ")
#print(content)

#content =["coronavirus, sars-cov-2, sars-cov2, sars cov 2,covid19, covid-19, covid 19, covid" ] 
print("Configuring Index Settings...")
## index settings: mapping for publish_time
doc_settings = {
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
                "acronym": {
                    "type": "word_delimiter",
                    "catenate_all": True,
                    "generate_word_parts": False,
                    "generate_number_parts": False,
                    "preserve_original": True
                },
                "my_snow":{
                    "type": "snowball",
                    "language": "English"
                },
                "english_stemmer" : {
                    "type" : "stemmer",
                    "language" : "english"
                },
              "keyword_list": {
                "type": "keyword_marker",
                "ignore_case": True,
                "keywords": ["covid-19", "sars-cov-2", "sars-cov", "2019-ncov",
                         "united states", "united kingdom", "hong kong", "united arab emirates",
                         "non-social", "african-american",
                          "mrna ", "ace inhibitor", "enzyme inhibitors", "blood type", "angiotensin-converting", "clinical signs", "super spreaders", "hand sanitizer", "alcohol sanitizer"]#
                 },
                "ngram_filter": {
                    "type":     "ngram",
                    "min_gram": 3,
                    "max_gram": 3,
                    "token_chars": [
                        "letter",
                        "digit",
                        "punctuation",
                        "symbol"
                    ]
                }
            },# FILTER END
            "char_filter": {
                "covid_char_filter": {
                "type": "mapping",
                            "mappings": [
                                "$=> dollar",
                                "€=> euro",
                                "£=> pound",
                                "%=> percentage"
                                ]
                }
             },
             #},# INDEX END
            "analyzer": {
                "covid_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "stopwords": "_english",
                    "filter": ["synonym",
                               "lowercase",
                                "keyword_list",
                               "stop",
                               "asciifolding",
                               "my_snow"
                               ],
                    "char_filter": ["covid_char_filter"]
                },
                "ngram_analyzer": {
                    "type":      "custom",
                    "tokenizer": "standard",
                    "filter":   [
                        "lowercase",
                        "ngram_filter"
                    ]
                },
                "query_analyzer":{
                    "type": "custom",
                    "tokenizer": "standard",
                    "stopwords": "_english",
                    "filter": ["lowercase",
                               "keyword_list",
                               "stop",
                               "asciifolding",
                               "my_snow"
                               ],
                    "char_filter": ["covid_char_filter"]
                    }
                }# ANALYZER END
        },# ANALYSIS END
    #SIMILARITY MODULE
    "similarity" : {
               "BM25_similarity": {
                    "type": "BM25",
                    "k1": "1.2", #the higher, the more relevant TF
                    "b": "0.75" #the higher, the higher the impact of document length
                  },
                  "DFR_similarity": {
                    "type": "DFR",
                    "basic_model": "g",
                    "after_effect": "l",
                    "normalization": "h2"
                  },
                  "LMJelinekMercer_short": {
                    "type": "LMJelinekMercer",
                    "lambda": "0.1"
                  },
                 "LMJelinekMercer_long": {
                    "type": "LMJelinekMercer",
                    "lambda": "0.7"
                  },
                "TFIDF": {
                    "type": "scripted",
                    "script": {
                    "source": "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
                    }
                }
        }#SIMILARITY END
    },# SETTINGS END

    "mappings": {
        "properties": {
            "title": { 
                "type": "text",
                "fields": {
                    "analysis": { 
                        "type":     "text",
                        "analyzer": "covid_analyzer",
                        "similarity": "BM25_similarity"
                    },
                    "ngram": { 
                        "type":     "text",
                        "analyzer": "ngram_analyzer",
                        "similarity": "BM25_similarity"
                    },
                    "keyword": { 
                        "type":     "keyword"
                    }
                }
            },
            "abstract": {
                "type": "text",
                "analyzer": "covid_analyzer",
                "similarity": "DFR_similarity"
            },
            "publish_time": {
                "type": "date"
            },
            "query": {
                "type": "text",
                "analyzer": "query_analyzer"
            }
        } # PROPERTIES END
    } # MAPPINGS END
}# DOC_SETTINGS END
print("Index Config Complete!...")

## Create Index
print("Creating Index...")
es.indices.create(index=index_name, ignore=400, body=doc_settings)
es.indices.analyze(index=index_name, ignore=400, body=doc_settings)

## Index Documents
print("Inserting Metadata into Index...")
with open("./Final_Build/metadata.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index=index_name,raise_on_error=False, stats_only=False)
print("Insert Complete! Pipeline end!")