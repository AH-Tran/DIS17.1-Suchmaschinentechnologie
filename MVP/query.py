from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import json

path = 'topics-rnd5_covid-complete.xml'
collection_name = "default_index"

def import_querys(path):
    tree = ET.parse(path)
    root = tree.getroot()
    query_list = []
    for topic in root:
        for querys in topic.findall("query"):
            query_list.append(querys.text)

    formatted_query_list = []
    for i in range(50):
        query = {"query": {"multi_match": {"query": query_list[i], "fields": ["title", "abstract"]}}}
        formatted_query_list.append(query)

    return formatted_query_list


liste = import_querys(path)


def search(collection_index, formatted_query_list):

    liste_strings = []
    #myfile = open("results.txt", 'w')
    for i in range(len(formatted_query_list)):
        elastic_client = Elasticsearch()
        response = elastic_client.search(index=collection_index, body=json.dumps(formatted_query_list[i]), size=50)

        #print("Num\titeration\t\tTitle\t\tRelevance Score")
        for idx, hit in enumerate(response['hits']['hits']):
            string = str(i+1) + " " + "Q0" + " " + str(hit['_source']['cord_uid']) + " " + str(idx) + " " + str(hit['_score']) + " Standard"
            liste_strings.append(string)

    myfile = open("results.txt", 'w', encoding="utf-8", newline='\n')

    for i in range(len(liste_strings)):
        myfile.write(liste_strings[i] + "\n")
    myfile.close()

search(collection_name, liste)