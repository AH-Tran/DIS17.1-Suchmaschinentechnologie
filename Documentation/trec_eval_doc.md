
###  Trec_Eval_Doc
Evaluate **qrel_file** with **results_file**    
```
```html
$ ./trec_eval [-q] [-m measure] qrel_file results_file
```
**trec_eval format**
- topic-id: ​ID oder Nummer des Topics aus der Topics Datei
- iteration​ (muss für TREC_EVAL vorhanden sein, hat aber keine Aussage für uns)
- cord-doc-id: ​ID des Dokuments aus der Collection (aus CORD-19 metadata.csv)
- judgment: ​Beurteilung ob das Dokument relevant für das Topic ist.
	- 0 := irrelevant
	- 1 := partially relevant
	- 2 := relevant
