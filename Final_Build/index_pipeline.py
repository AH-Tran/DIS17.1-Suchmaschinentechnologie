from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from datetime import datetime
import os, uuid
import pandas as pd
import json
import requests 
import sys
import jsonlines

# json files directory
directory = 'D:\Creation\Programming\documents' 
## Connect to Elasticsearch
res = requests.get('http://localhost:9200')

es = Elasticsearch([{"host": "localhost", "port": 9200}])

index_name= "livivo_index"

## Check if Index already exists
if es.indices.exists(index_name):
    es.indices.delete(index=index_name)

with open(".\Final_Build\synonyms_final.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
for i in content:
    i.replace("_", " ")
#print(content)


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
                "keywords": ["Vitamin D", "covid-19", "sars-cov-2", "sars-cov", "2019-ncov",
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
                                "acronym",
                               "lowercase",
                                "keyword_list",
                               "stop",
                               "asciifolding",
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
                    "filter": ["keyword_list",
                               "stop",
                               "asciifolding"
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
                    "basic_model": "g",#possible values: g, if, in, ine
                    "after_effect": "b",#possible values: b, l
                    "normalization": "z" #possible values: no, h1, h2, h3, z
                  },
                  "LMJelinekMercer_short": {
                    "type": "LMJelinekMercer",
                    "lambda": "0.1" #The closer to 0, the better score for documents with many query matches
                  },
                 "LMJelinekMercer_long": {
                    "type": "LMJelinekMercer",
                    "lambda": "0.7" #The closer to 0, the better score for documents with many query matches
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
            "TITLE": { 
                "type": "text",
                "fields": {
                    "analysis": { 
                        "type":     "text",
                        "analyzer": "covid_analyzer",
                        "similarity": "LMJelinekMercer_short"
                    },
                    "ngram": { 
                        "type":     "text",
                        "analyzer": "ngram_analyzer",
                        "similarity": "LMJelinekMercer_short"
                    },
                    "keyword": { 
                        "type":     "keyword"
                    }
                }
            },
            "ABSTRACT": {
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
"""
def load_json(directory):
    " Use a generator, no need to load all in memory"
    for filename in os.listdir(directory):
        if filename.endswith('.jsonl'):
            fullpath = os.path.join(directory, filename)
            with open(fullpath,'r', encoding= 'ascii') as open_file:
                reader = jsonlines.Reader(open_file)
                print(reader)
helpers.bulk(es, load_json("D:\Lilias\DIS17.1-Suchmaschinentechnologie\livivo\documents"), index=index_name, raise_on_error=False, stats_only=False)
"""

print("Inserting Metadata into Index...")
"""

i = 1
for filename in os.listdir('D:\Lilias\DIS17.1-Suchmaschinentechnologie\livivo'):
    if filename.endswith(".jsonl"):
        fullpath = os.path.join(directory, filename)
        f = open(fullpath)
        docket_content = f.read()
        #sending data into elasticsearch
        es.bulk(index = index_name, ignore = 400, doc_type = 'docket', id = i, body = json.loads(docket_content))
        i = i + 1
"""

## Index Documents
print("Inserting Metadata into Index...")
with open("D:\Creation\Programming\documents\livivo_nlm.jsonl", "r", encoding="utf8") as f:
    reader = jsonlines.Reader(f)
    helpers.bulk(es, reader, index=index_name,raise_on_error=False, stats_only=False)
print("Insert Complete! Pipeline end!")