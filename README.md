# Readme_Masterfile 
### 0- TO DO
- [X] [https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html]
	- [X] Read: Custom_analyzer for Tokens, Filters, ETC
	- [X] Create Index_pipeline.py for indexing metadata.csv with Custom_analyzer 
	- [X] Apply Custom_analyzer to Querybuilder
	- [X] Read up on Ingestion Nodes (Tran)

### 1. MVP
- [x] Install Elastic + Kibana
- [x] Install trec_eval
- [x] Import metadata.csv into Kibana
- [x] Index metadata.csv
- [x] Execute all 50 queries in topic on metadata.csv
- [x] Import search results
- [x] Transform search results into [trec_eval_format](https://github.com/AH-Tran/DIS17.1-Suchmaschinentechnologie/blob/main/Documentation/trec_eval_doc.md)
- [x] Evaluate search results with trec_eval

### 2. Further Development
- [X] Apply **3. How to improve Rankings**
- [X] Automate with Python + Jupiter Notebook
	- [X] Query to Elastic
	- [X] Get Search Result from Elastic
	- [X] Transform Result into trec_eval format
	- [X] Union the results into one result file
	- [X] Evaluate result file with trec_eval

###  3. How to improve Rankings
- [X] Indexing
- [X] Stopword Lists
	- [X] Analyse Metadata.csv
	- [X] Most frequent words
	- [X] Most rare words with high frequency in single documents
	- [X] Stopword_list for different languages
		- [X] Identify Languages with [https://github.com/saffsd/langid.py](https://github.com/saffsd/langid.py)
		- [X] NLP Tool [https://spacy.io/](spacy)
		- [X] NLTK library [https://www.nltk.org/](https://www.nltk.org/)
	- [X] Vereinigen mit nltk_stopwords.txt
	- [X] Inverse Application of diffferent stopword_lists for different languages
- [X] Thesauri (Synonym, Polysemi)
	- [X] [https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html)
	- [X] [https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-graph-tokenfilter.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-graph-tokenfilter.html)
- [X] Tokenization
	- [X] first 10(?) tokenz sum up most of the text
	- [X] Zipfl-Curve
	- [X] [https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.htmlt](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.htmlt)
- [X] Casefolding
	- [X] [https://drowning.gitbooks.io/elasticsearch/content/220_Token_normalization/40_Case_folding.html](https://drowning.gitbooks.io/elasticsearch/content/220_Token_normalization/40_Case_folding.html)
- [X] Stemming
	- [X] -   [https://www.elastic.co/guide/en/elasticsearch/reference/current/stemming.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/stemming.html)
- [X] Weights
	- [X] Genetic Algorithm
### 4. Documentation
Document development with LateX
- [X] General Project Structure
- [X] Approach and Models to improve Results
- [X] Evaluation Results
- [X] Discussion of Results
- [X] Future Improvement
- [X] Literature & References

**Overleaf Latex Project:**  
https://www.overleaf.com/project/5f881fd0d2a2ac0001ba9af3  
Email: Dis17_search@outlook.com  
PW: zsh17seo  
**Project Timeline:**  
https://app.asana.com/0/1198889708166349/list

### 6. Presentation

https://drive.google.com/file/d/159reGm6GmrpRyARyYomXdJFnLFZ5mx92/view?usp=sharing

### 7. Literature
- [https://qa.fastforwardlabs.com/elasticsearch/qa%20system%20design/passage%20ranking/masked%20language%20model/word%20embeddings/2020/07/22/Improving_the_Retriever_on_Natural_Questions.html](https://qa.fastforwardlabs.com/elasticsearch/qa%20system%20design/passage%20ranking/masked%20language%20model/word%20embeddings/2020/07/22/Improving_the_Retriever_on_Natural_Questions.html)
- [https://qa.fastforwardlabs.com/elasticsearch/mean%20average%20precision/recall%20for%20irqa/qa%20system%20design/2020/06/30/Evaluating_the_Retriever_&_End_to_End_System.html](https://qa.fastforwardlabs.com/elasticsearch/mean%20average%20precision/recall%20for%20irqa/qa%20system%20design/2020/06/30/Evaluating_the_Retriever_&_End_to_End_System.html)

### MISC > Interesting Examples:
Elastic + Trec_Eval as with complete frontend+backend with vue
[https://git.informatik.uni-leipzig.de/js35jisu/recipe-search2](https://git.informatik.uni-leipzig.de/js35jisu/recipe-search2)

Treceval
[https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjAjPrVqs_sAhXO_KQKHQpnB0EQFjAAegQIBBAC&url=https%3A%2F%2Fgithub.com%2Fjoaopalotti%2Ftrectools&usg=AOvVaw2-K4AC-wm_kih4h9jwMCAX](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjAjPrVqs_sAhXO_KQKHQpnB0EQFjAAegQIBBAC&url=https%3A%2F%2Fgithub.com%2Fjoaopalotti%2Ftrectools&usg=AOvVaw2-K4AC-wm_kih4h9jwMCAX)

Pythonscripting with elastic
[https://qbox.io/blog/python-scripts-interact-elasticsearch-examples](https://qbox.io/blog/python-scripts-interact-elasticsearch-examples)

[https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html#modules-scripting-stored-scripts](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html#modules-scripting-stored-scripts)

Evaluating Elastic
[https://www.elastic.co/blog/made-to-measure-how-to-use-the-ranking-evaluation-api-in-elasticsearch](https://www.elastic.co/blog/made-to-measure-how-to-use-the-ranking-evaluation-api-in-elasticsearch)

Synonyms in Elastic
[https://www.elastic.co/blog/boosting-the-power-of-elasticsearch-with-synonyms?iesrc=rcmd&astid=a097870a-3dda-4289-acd4-2210d05cb1ed&at=58&rcmd_source=WIDGET&req_id=45be7f2d-46ec-476e-ab02-2d72778d055d](https://www.elastic.co/blog/boosting-the-power-of-elasticsearch-with-synonyms?iesrc=rcmd&astid=a097870a-3dda-4289-acd4-2210d05cb1ed&at=58&rcmd_source=WIDGET&req_id=45be7f2d-46ec-476e-ab02-2d72778d055d)

Searchrequest API(Java)
[https://www.elastic.co/guide/en/elasticsearch/client/java-rest/current/java-rest-high-search.html#java-rest-high-search-request-building-queries](https://www.elastic.co/guide/en/elasticsearch/client/java-rest/current/java-rest-high-search.html#java-rest-high-search-request-building-queries)

Querystrings(Elastic)
[https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html)

Covid19 Protein Thesaurus  

[https://www.cas.org/covid-19-thesaurus-completed](https://www.cas.org/covid-19-thesaurus-completed)
