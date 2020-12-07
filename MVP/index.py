from elasticsearch import helpers, Elasticsearch
import csv

es = Elasticsearch()
es.indices.delete(index='my-index', ignore=[400, 404])

doc_setting = {
    "settings": {
        "analysis": {
            "filter": {
                "stopwordEn": {
                    "type":       "stop",
                    "stopwords":  "english"
                    
                }
            }
        }
    },
  "mappings": {
    "hits": {
        "hits":{
      "properties": {
        "abstract": {
          "type": "string",
          "analyzer": "custom_lowercase_stemmed"
        }
      }
    }
  }
}
}
es.indices.create(index='my-index', body=doc_setting, ignore=[400, 404])
es.indices.analyze(index='my-index', body=doc_setting)

with open("C:/Users/Constantin/Desktop/Suchmaschinen/composer/metadata.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='my-index',raise_on_error=False, stats_only=False)

    
    #helpers.bulk(es, reader, index='my-index',raise_on_error=False, stats_only=False, ) # raise_on_error=False # stats_only=False #doc_type='Articles'