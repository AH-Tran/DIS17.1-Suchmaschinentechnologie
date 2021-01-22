# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:52:14 2021

@author: joshu
"""

import pandas as pd

df = pd.read_csv("cluster_all_csv.csv", names=["quatsch","cord_uid","cluster"])
df = df.drop("quatsch", axis=1)
df = df.drop_duplicates(["cord_uid"])
df2 = pd.read_csv("metadata_update.csv")

df_final = df.merge(df2, left_on='cord_uid', right_on='cord_uid', how='right')

df_final.to_csv("added_cluster.csv", index = False)