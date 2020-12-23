from elasticsearch import Elasticsearch
from elasticsearch_dsl import analyzer
import xml.etree.ElementTree as ET
import json

path = 'topics-rnd5_covid-complete.xml'
collection_name = "covid_index"
'''
settings = {
    "settings": {
        # just one shard, no replicas for testing
        "number_of_shards": 1,
        "number_of_replicas": 0,

        # custom analyzer for covid metadata.csv
        "analysis": {
            "analyzer": {
                "covid_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "stopwords": "_english",
                    "filter": ["lowercase",
                               "stop",
                               "asciifolding"
                               ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "query": {
                "type": "text",
                "analyzer": "covid_analyzer"
            }
        }
    }
}
'''

def import_querys(path):
    tree = ET.parse(path)
    root = tree.getroot()
    query_list = []
    narrative_list = []
    question_list = []
    for topic in root:
        for querys in topic.findall("query"):
            query_list.append(querys.text)
        for narratives in topic.findall("narrative"):
            narrative_list.append(narratives.text)
        for questions in topic.findall("question"):
            question_list.append(questions.text)

    # test_analyzer = analyzer("test_analyzer", type="custom", tokenizer="standard", stopwords="_german",
    #                          filter=["lowercase","stop","asciifolding"])

    formatted_query_list = []
    for i in range(50):
        query = {"query": {
            "bool":{
                "should":{
                    "multi_match": {
                        "query": query_list[i],
                        "analyzer": "covid_analyzer",
                        "fields": ["title", "abstract"]},
                    "multi_match":{
                        "query": question_list[i],
                        "analyzer": "covid_analyzer",
                        "fields": ["title", "abstract"]},
                    "multi_match": {
                        "query": narrative_list[i],
                        "analyzer": "covid_analyzer",
                        "fields": ["title", "abstract"]}
                }
                }
        }
}


        '''
        query = {
            "query": {
                "bool": {
                    "must": {
                        "query_string":{
                            "query": query_list[i],
                            "analyzer": "covid_analyzer",
                            "fields": ["title", "abstract"]}},
                    "should": [
                        {
                            "range": {
                                "publish_date": {
                                    "boost": 1,
                                    "gte": "2019-12-01 00:00:00"
                                }
                            }
                        },
                        {
                            "range": {
                                "publish_date": {
                                    "lt": "1900-01-01 00:00:00",
                                    "boost": 0.1
                                }
                            }
                        }
                    ]
                }
            }
        }
        '''
        formatted_query_list.append(query)

    return formatted_query_list


liste = import_querys(path)


# print(liste[0])

def search(collection_index, formatted_query_list):
    liste_strings = []
    # myfile = open("results.txt", 'w')
    for i in range(len(formatted_query_list)):
        id_list = []
        elastic_client = Elasticsearch()
        response = elastic_client.search(index=collection_index, body=json.dumps(formatted_query_list[i]),
                                         size=1000)

        # print("Num\titeration\t\tTitle\t\tRelevance Score")
        for idx, hit in enumerate(response['hits']['hits']):
            if str(hit['_source']['cord_uid']) not in id_list:
                id_list.append(hit['_source']['cord_uid'])
                string = str(i + 1) + " " + "Q0" + " " + str(hit['_source']['cord_uid']) + " " + str(idx) + " " + str(
                    hit['_score']) + " Standard"
                liste_strings.append(string)
            else:
                continue
    myfile = open("results_full_information.txt", 'w', encoding="utf-8", newline='\n')

    for i in range(len(liste_strings)):
        myfile.write(liste_strings[i] + "\n")
    myfile.close()


search(collection_name, liste)
