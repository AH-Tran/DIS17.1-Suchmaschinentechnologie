from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from elasticsearch.client.ingest import IngestClient
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

index_name= "livivo_index_test"
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
with open("D:\Creation\Programming\documents\livivo_testset.jsonl", "r", encoding="utf8") as f:
    reader = jsonlines.Reader(f)
    helpers.bulk(es, reader, index=index_name,raise_on_error=False, stats_only=False)
print("Insert Complete! Pipeline end!")