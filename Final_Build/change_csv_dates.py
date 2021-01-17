import pandas as pd
import re
import pprint
import datetime
pd.options.mode.chained_assignment = None

df = pd.read_csv("./Final_Build/metadata.csv")
#liste = df["publish_time"]
#print(liste[0])


#print(liste[0:15])
pattern_date_1 = re.compile(r'^\d\d\d\d-\d\d-\d\d$')
pattern_date_2 = re.compile(r'^\d\d\d\d$')
#pattern_date_3 = re.compile(r'^$')
datums_liste = ["2020-04-01","2020-01-01", "2020-04-01", "2020-04-10", "2020-08-06","2020-07-28","2020-02-25","2020-01-24", "2020-05-18","2020-05-01",
                "2020-01-01","2020-03-30", "2021-04-01", "2020-03-12", "2021-08-01", "2020-01-28", "2020-01-30","2020-07-28"]

liste_date_1 = []
liste_date_2 = []
liste_date_3 = []

for i in range(len(df["publish_time"])):
    if pattern_date_1.match(str(df["publish_time"][i])):
        continue
    elif pattern_date_2.match(str(df["publish_time"][i])):
        df["publish_time"][i] = df["publish_time"][i].replace(str(df["publish_time"][i]),str(df["publish_time"][i]) + "-01-01" )
    else:
        for j in datums_liste:
            df["publish_time"][i] = j


for i in range(len(df["publish_time"])):
    if pattern_date_1.match(str(df["publish_time"][i])):
        continue
    elif pattern_date_2.match(str(df["publish_time"][i])):
        continue
    else:
        liste_date_3.append(df["title"][i])

#print("Gesamte Daten:", len(liste))
print("Daten mit kompletten Zeitformat:", len(liste_date_1))
print("Daten (nur Jahreszahl):", len(liste_date_2))
print("Kein Datum:",len(liste_date_3))

print(liste_date_3)
#print(len(liste_date_1) +len(liste_date_2)+len(liste_date_3))
#print(len(liste)-(len(liste_date_1) +len(liste_date_2)+len(liste_date_3)))

df.to_csv("./Final_Build/metadata_update.csv")