from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import json

path = './Final_Build/topics-rnd5_covid-complete.xml'
collection_name = "covid_index"


def import_querys(path):
    tree = ET.parse(path)
    root = tree.getroot()
    query_list = []
    narrative_list = []
    question_list = []
    for topic in root:
        for querys in topic.findall("query"):
            query_list.append(querys.text)
        # for narratives in topic.findall("narrative"):
        #   narrative_list.append(narratives.text)
        # for questions in topic.findall("question"):
        #  question_list.append(questions.text)

    formatted_query_list = []
    '''
    for i in range(50):
        query = {
            "query": {
                "bool": {
                    "should": {
                        "multi_match": {
                            "query": query_list[i],
                            "analyzer": "query_analyzer",
                            "fields": ["title.analysis^2", "title^0.8", "title.keyword^10"]},

                        "multi_match": {
                            "query": query_list[i],
                            "analyzer": "query_analyzer",
                            "fields": "title.ngram^0.5",
                            "minimum_should_match": "80%"}
                    }
                }
            }
        }
        '''
    for i in range(50):
        query = {
            "query": {
                "multi_match": {
                    "query": query_list[i],
                    "analyzer": "query_analyzer",
                    "fields": ["title.analysis^2", "title^0.8", "title.keyword^10"]}
            }
        }

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
                                         size=1000, request_timeout=(100))

        # print("Num\titeration\t\tTitle\t\tRelevance Score")
        for idx, hit in enumerate(response['hits']['hits']):
            if str(hit['_source']['cord_uid']) not in id_list:
                id_list.append(hit['_source']['cord_uid'])
                string = str(i + 1) + " " + "Q0" + " " + str(hit['_source']['cord_uid']) + " " + str(idx) + " " + str(
                    hit['_score']) + " Standard"
                liste_strings.append(string)
            else:
                continue
    myfile = open("./Final_Build/result_files/results_002.txt", 'w', encoding="utf-8", newline='\n')

    for i in range(len(liste_strings)):
        myfile.write(liste_strings[i] + "\n")
    myfile.close()


search(collection_name, liste)
print("Result finished! END")