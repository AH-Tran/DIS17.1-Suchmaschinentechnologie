from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import json
import jsonlines
import re

path = 'D:\Creation\Programming\candidates\livivo_hq_test_100.jsonl'

collection_name = "livivo_index"

print("Defining Query...")
def import_querys(path):
    query_list = []
    with open(path, 'r', encoding= 'utf-8') as f:
        queries = jsonlines.Reader(f)
        for i in queries:
            #query_list.append(re.sub(r'([a-z]+)', r'(\1)', i['qstr']))
            query_list.append(i['qstr'].replace('AND', '+').replace('OR','|'))
            print(query_list)

    formatted_query_list = []
    for i in range(100):
    
        query = {
            "query": {
                "simple_query_string": {
                    "query": query_list[i],
                    "analyzer": "query_analyzer",
                    "fields": ["TITLE.analysis", "TITLE", "TITLE.keyword"]},
                
                 "simple_query_string": {
                     "query": query_list[i],
                     "analyzer": "query_analyzer",
                     "fields": ["ABSTRACT"]},
                 
                 "simple_query_string": {
                     "query": query_list[i],
                     "analyzer": "query_analyzer",
                     "fields": ["MESH"]}}
                

            }
                        
                                

        formatted_query_list.append(query)

    return formatted_query_list


liste = import_querys(path)

path2 = 'D:\Creation\Programming\candidates\livivo_hq_test_100_candidates.jsonl'

# print(liste[0])
print("Post Query...")
def search(collection_index, formatted_query_list):
    liste_strings = []
    candidates = []
    with open(path2, 'r', encoding= "utf-8") as f:
        candidates2 = jsonlines.Reader(f)
        for i in candidates2:
            candidates.append(i['candidates'])
    # myfile = open("results.txt", 'w')
    for i in range(len(formatted_query_list)):
        id_list = []
        candidates_list = []
        elastic_client = Elasticsearch()
        response = elastic_client.search(index=collection_index, body=json.dumps(formatted_query_list[i]),
                                         size=100, request_timeout=(100))

        # print("Num\titeration\t\tTitle\t\tRelevance Score")
        for idx, hit in enumerate(response['hits']['hits']):
            if str(hit['_source']['DBRECORDID']) not in id_list:
                id_list.append(hit['_source']['DBRECORDID'])
                string = str(i + 1001) + " " + "Q0" + " " + str(hit['_source']['DBRECORDID']) + " " + str(idx) + " " + str(
                    hit['_score']) + " Standard"
                liste_strings.append(string)
                candidates_list.append(str(hit['_source']['DBRECORDID']))
            else:
                continue
        test_list = list(set(candidates[i]).intersection(set(candidates_list))) 
        print(len(test_list))
        #print(candidates[i])
        
        
    myfile = open("results_livivo.txt", 'w', encoding="utf-8", newline='\n')

    for i in range(len(liste_strings)):
        myfile.write(liste_strings[i] + "\n")
    myfile.close()
    
print("Writing Results in results.txt...")

search(collection_name, liste)
print("Result finished! END")


print("calculating intersection")

