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
    - Which Stemmer is ideal? Snow or Standardstemmer
2. BM25: Which Parameters are the best? (For All Fields)
3. DFR: Which Parameters are the best? ( in Abstract)
4. LMJ: Which Paramameters are the best? (in Abstract & Title)
5. Similarity Module Testing for Title: Which is best? (BM25 vs. LMJ Short, vs TFIDF)
6. Similarity Module Testing for Abstract: (BM25 vs. DFR vs. LMJ Short vs TFIDF)
7. Put Together best results
8. Boosting: Testing best Parameters for title
10. Boosting: Testing best Parameters for abstract
11. Boosting: Testing best Parameter for n_gram> minimum_should_match %
12. Boosting: Testing best Parameters for publish_time
13. Adjust Synonyms, is it better?