from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from datetime import datetime
import os
import pandas as pd
import csv
import itertools
import json
import requests

## Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

## Generate CSV Dataframe
csv_df = pd.read_csv('metadata.csv', dtype=str, encoding='utf-8')

## Get all Data Fields
column_list = csv_df.columns.to_list()

## Get rid of all missing Values, change to "none"
for col in column_list:
    csv_df.loc[csv_df[col].isnull(), col] = "None"

## Transform Dataframe to Dictionary
documents = csv_df.to_dict(orient='records')

## Check if Index already exists
if es.indices.exists("covid_index"):
    es.indices.delete(index="cord")

## index settings: mapping for publish_time
settings={
    "settings": {},
    "mappings": {
        "properties": {
            "publish_time": {
                "type": "text"
            }
        }
    }
}

## Create Index
es.indices.create(index="covid", ignore=400, body=settings)

## Index Documents
bulk(es, index='cord', doc_type='_doc', request_timeout=60, raise_on_error=True)