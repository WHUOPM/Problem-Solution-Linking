# Problem-Solution-Linking
==============================
Identify problems and solutions of research articles and predict new solutions given a problem based on known knowledge.

## Framework of experiments
--------------
* Representation: extract main problem and main solution from an article.
* Construction: construct a bipartite graph based on problem and solution pairs.
* Prediction: predict new problem and solution pairs based on constructed graph.


### Representation
------------
Knowledge is the result of solving problems, papers are knowledge carrier recording solutions of problems. A Paper can be represented with a problem and solution pair. To represent a paper with its problem and solution, we should first extract entities representing problem and entities representing solution. The main assumption is that problem entities or solution entities that appears in title are main problem and main solution. So the problem has been converted to a classification problem of which task is to classify whether a problem entity or solution entity in abstract is main problem or solution of that articles.
The main procedures are listed as follows:

1. Identify problem entities and solution entities from abstract of research articles. 
	In this step, we apply [Stanford entity learning method](http://nlp.stanford.edu/software/patternslearning.shtml) based on [SPIE](http://nlp.stanford.edu/pubs/gupta-manning-ijcnlp11.pdf) to extract two kinds of entities (Problem and Solution) from articles' abstract.

2. Training data construction
	
