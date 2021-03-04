from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import json
import jsonlines
import re

path = 'D:\Creation\Programming\candidates\livivo_hq_1000.jsonl'
path2 = 'D:\Creation\Programming\candidates\livivo_hq_100_candidates.jsonl'

collection_name = "livivo_index_2json"
result_file = './Final_Build/result_files/results_livivo_candidates_only.txt'

print("Defining Query...")
def import_querys(path):
    query_list = []
    with open(path, 'r', encoding= 'utf-8') as f:
        queries = jsonlines.Reader(f)
        for i in queries:
            #query_list.append(re.sub(r'([a-z]+)', r'(\1)', i['qstr']))
            query_list.append(i['qstr'].replace('AND', '+').replace('OR','|'))
            #print(query_list)

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
        query_string_list = []
        elastic_client = Elasticsearch()
        response = elastic_client.search(index=collection_index, body=json.dumps(formatted_query_list[i]),
                                         size=10000, request_timeout=(100))
        # print("Num\titeration\t\tTitle\t\tRelevance Score")
        for idx, hit in enumerate(response['hits']['hits']):
            if str(hit['_source']['DBRECORDID']) not in id_list and str(hit['_source']['DBRECORDID']) in candidates[i]:
                id_list.append(hit['_source']['DBRECORDID'])
                string = str(i + 1001) + " " + "Q0" + " " + str(hit['_source']['DBRECORDID']) + " " + str(("&&&")) + " " + str(
                    hit['_score']) + " Standard"
                query_string_list.append(string)
                candidates_list.append(str(hit['_source']['DBRECORDID']))
            else:
                continue
        test_list = list(set(candidates[i]).intersection(set(candidates_list)))
        test_list_2 = list(set(candidates[i])-set(test_list))
   
        for j in range(len(test_list_2)):
                string = str(i + 1001) + " " + "Q0" + " " + str(test_list_2[j]) + " " + str("&&&") + " " + str(
                            0.01) + " Standard"
                query_string_list.append(string) 

        for k in range(len(query_string_list)): 
            xy = str(k)
            query_string_list[k]= query_string_list[k].replace("&&&", xy)
        liste_strings.append(query_string_list)
            #k = str(k)
            #liste_strings = [l.replace('&&&', k) for l in liste_strings]
        
        #print(len(test_list))
        #print(candidates[i])
        

    myfile = open(result_file, 'w', encoding="utf-8", newline='\n')
    flat_list = [item for sublist in liste_strings for item in sublist]
    for i in range(len(flat_list)):
        myfile.write(flat_list[i] + "\n")
    myfile.close()
    
print("Writing Results in results.txt...")

search(collection_name, liste)
print("Result finished! END")


print("calculating intersection")

