from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import json
import pandas as pd
pd.options.mode.chained_assignment = None

path = 'topics-rnd5_covid-complete.xml'
collection_name = "covid_index_test"

print("Defining Query...")


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
    for i in range(50):
        query = {
            "query": {
                "bool": {
                    "must": {
                        "bool": {
                            "should": [{
                                "multi_match": {
                                    "query": query_list[i],
                                    "analyzer": "query_analyzer",
                                    "fields": ["title.analysis^1.5", "title^1", "title.keyword^5"]}},
                                {
                                "multi_match": {
                                    "query": query_list[i],
                                    "analyzer": "query_analyzer",
                                    "fields": "title.ngram^0.5",
                                    "minimum_should_match": "80%"
                                }
                            },
                                {
                                    "multi_match": {
                                        "query": query_list[i],
                                        "analyzer": "query_analyzer",
                                        "fields": "abstract",
                                        "boost": 8}
                                }]}},
                    "should": [
                        {
                            "range": {
                                "publish_time": {
                                    "boost": 1.2,
                                    "gte": "2020-01-01"
                                }
                            }
                        },
                        {
                            "range": {
                                "publish_time": {
                                    "lt": "2020-01-01",
                                    "boost": 0.8
                                }
                            }
                        }
                    ]

                }
            }
        }

        formatted_query_list.append(query)

    return formatted_query_list


liste = import_querys(path)

# print(liste[0])
print("Post Query...")


def reranking(liste, iterator):
    print(iterator)
    df_1 = pd.read_csv("cluster_all_csv.csv", names=["quatsch", "cord_uid", "Cluster"]).drop("quatsch", axis=1)
    df = df_1.drop_duplicates(subset=["cord_uid"])
    data = pd.DataFrame(liste, columns=["Q0_col", "cord_uid", "Ranking", "Score", "Standard"])

    # data = pd.read_csv('results_001_synonyms_final.txt', sep=" ",
    #                   names=["Q0_col", "cord_uid", "Ranking", "Score", "Standard"], nrows=983)
    df_new = df.merge(data, left_on="cord_uid", right_on="cord_uid", how="right").sort_values(by=["Ranking"])

    test = df_new["Cluster"][0:50].value_counts().index.values
    test_2 = df_new["Cluster"][0:50].value_counts().values

    percentile_list = pd.DataFrame({'Cluster': test, 'amount': test_2})

    df_new_2 = df_new.merge(percentile_list, right_on="Cluster", left_on="Cluster", how="left")
    # print(df_new_2[50:55])

    for key, value in df_new_2.iterrows():
        #if 10 <= df_new_2["amount"][key] < 20:
        #    df_new_2["Score"][key] = df_new_2["Score"][key] * 1.01
        #elif 20 <= df_new_2["amount"][key] < 30:
        #    df_new_2["Score"][key] = df_new_2["Score"][key] * 1.02
        #elif 30 <= df_new_2["amount"][key] < 40:
        #    df_new_2["Score"][key] = df_new_2["Score"][key] * 1.03
        if 40 <= df_new_2["amount"][key] < 50:
            df_new_2["Score"][key] = df_new_2["Score"][key] * 1.04
        elif df_new_2["amount"][key] >= 50:
            df_new_2["Score"][key] = df_new_2["Score"][key] * 1.05

    df_new_3 = df_new_2.sort_values(by=["Score"], ascending=False).reset_index()

    ergebnis_liste = []

    for key, value in df_new_3.iterrows():
        string = str(iterator + 1) + " " + "Q0" + " " + value["cord_uid"] + " " + str(key) + " " + str(
            value["Score"]) + " " + "Standard"
        ergebnis_liste.append(string)

    return ergebnis_liste


def search(collection_index, formatted_query_list):
    liste_strings = []

    # myfile = open("results.txt", 'w')
    for i in range(len(formatted_query_list)):
        id_list = []
        liste_df = []
        liste_strings_2 = []
        # id_list_2 = []
        elastic_client = Elasticsearch()
        response = elastic_client.search(index=collection_index, body=json.dumps(formatted_query_list[i]),
                                         size=1000, request_timeout=(100))

        # print("Num\titeration\t\tTitle\t\tRelevance Score")
        for idx, hit in enumerate(response['hits']['hits']):
            if str(hit['_source']['cord_uid']) not in id_list:
                id_list.append(hit['_source']['cord_uid'])
                #string = str(i + 1) + " " + "Q0" + " " + str(hit['_source']['cord_uid']) + " " + str(idx) + " " + str(
                #    hit['_score']) + " Standard"
                id_list_2 = ["Q0", str(hit['_source']['cord_uid']), idx, hit['_score'], " Standard"]
                liste_df.append(id_list_2)
                #liste_strings_2.append(string)
                #print(len(liste_strings_2))
                # liste_strings.extend(liste_reranked)
                #liste_strings.append(string)
            else:
                continue
        #print(idx)
        print(len(id_list))
        print(len(liste_df))
        liste_reranked = reranking(liste=liste_df, iterator=i)
        liste_strings.extend(liste_reranked)
    # liste = reranking(liste_df)
    myfile = open("reranking_test_3.txt", 'w', encoding="utf-8", newline='\n')

    for i in range(len(liste_strings)):
        myfile.write(liste_strings[i] + "\n")
    myfile.close()


# print("Writing Results in results.txt...")

search(collection_name, liste)
# print("Result finished! END")
