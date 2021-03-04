from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import json
import jsonlines
import re

path = 'D:\Creation\Programming\candidates\livivo_hq_test_100.jsonl'

collection_name = "livivo_index"
client = Elasticsearch("http://localhost:9200")
query = {
            "query": {
                "query_string" : {
                    "query": "(cardiovascular) AND (disease)",
                    "fields": ["TITLE^5", "ABSTRACT"],
                    "default_operator": "and"
                }
            }
}
# declare a query dict object for the explain() method call
#query = {"query": {"match" : {"string field" : "Object" }}}
print ("query:", query)

result = Elasticsearch.explain(client, index="livivo_index", id="oBL_4ncB1izoGxjRiSJT", body=query)
#print (json.dumps(result, indent=4))


# print the JSON response from Elasticsearch with indentations
print (json.dumps(result, indent=4))

# access the "explanation" and "description" keys
print ("explanation description:", result["explanation"]["description"])
# prints --> "description": "weight(string field:object in 0) [PerFieldSimilarity], result of:"

# print the "matched" key of the dict object
print ("query match:", result["matched"])