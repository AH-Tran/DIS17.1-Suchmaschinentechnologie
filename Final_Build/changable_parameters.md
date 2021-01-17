# Parameters

## analyzer
In Final_Build/index_pipeline.py
- tokenizer (https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html)
- filter:
    - Stemming
        - my_snow (aggressive)
        - english_stemmer (lax)

## ngram_filter
In Final_Build/index_pipeline.py
- min_gram (minimum size of each token)
- max_gram (maximum size of each token)

## synonym
In Final_Build/index_pipeline.py
- Evtl Covid-19 Synonyme weiter ergänzuen

## similiarity
- BM25_similarity
    - k1
    - b
- DFR_similarity
    - basic_model
    - after_effect
    - normalization
- LMJelinekMercer_short
    - lambda
- LMJelinekMercer_long
    - lambda
- TFIDF
    - script > source 

- mappings
    - properties
        - title
            - similarity
        - abstract
            - similarity

## Boosting
In Final_Build/query.py
- title
- title.analysis
- title.keyword
- title.ngram
    - minimum_should_match: xx%
- publish_time
    - Since 2019?

### Reranking Procedure
1. Similarity Module: All BM25, with standardized Boosts
    - Which Stemmer is ideal? Snow or Standardstemmer **> mit query.py**
2. BM25: Which Parameters are the best? (in Abstract & Title) **> mit query.py**
3. DFR: Which Parameters are the best? ( in Abstract) **> mit query_abstract.py**
4. LMJ: Which Paramameters are the best? (in Abstract & Title) **> mit query.py**
5. Similarity Module Testing for Title: Which is best? (BM25 vs. LMJ Short, vs TFIDF) **> mit query_title.py**
6. Similarity Module Testing for Abstract: (BM25 vs. DFR vs. LMJ Short vs TFIDF) **> mit query_abstract.py**
7. **Put Together best results**
8. Boosting: Testing best Parameters for title  **> mit query_title.py**
9. Boosting: Testing best Parameters for abstract **> mit query_abstract.py**
10. Boosting: Testing best Parameter for n_gram> minimum_should_match % **> mit query.py**
11. Boosting: Testing best Parameters for publish_time **> mit query.py**
12. **Put Together best boosting Parameters**
13. Adjust Synonyms, is it better? **> mit query.py**

Arbeitspaket 1: 1
Arbeitspaket 2: 2, 3, 4
Arbeitspaket 3: 5, 6
Arbeitspaket 4: 7
Arbeitspaket 5: 8, 9, 10, 11
Arbeitspaket 6: 12
Arbeitspaket 7: 13