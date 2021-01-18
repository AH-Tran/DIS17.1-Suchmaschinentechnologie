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
    - basic_model **g**
    - after_effect **b**
    - normalization **z**
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