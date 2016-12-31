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
	In this step, we apply [Stanford entity learning method](http://nlp.stanford.edu/software/patternslearning.shtml) based on [SPIED](http://nlp.stanford.edu/pubs/gupta-manning-ijcnlp11.pdf) to extract two kinds of entities (Problem and Solution) from articles' abstract.

	This is a bootstrapping method iteratively learning more entities and patterns by using some seeds.

	Seeds we use in this experiment are extracted from articles' title by using a special pattern "NN using NN". The first NN is  problem entity, the second NN is solution entity. We use this pattern to match article titles to generate problem seeds and solution seeds. 

	Input: acm articles' abstract. 
	Output: problem entities, solution entities, patterns 

2. Training data construction. 
	We treat the problem entities and solution entities that appear in titles as main problem and solution of that article. We could get many training data through this way. But there are still many other article of which titles do not include problem and solution entities. Our main mission is to identify main problem and solution from extracted problem entities and solution entities for these articles.

3. Model training and evaluation
	It could be treated as an binary classification problem. Features should be specified, and the method are from scikit-learn. We evaluate our method based on training set and  manually evaluate 200 files.

4. Extract problem and solution pairs of articles from acm dl.

### Construction
---------------
To construct a problem and solution bipartite graph, there still some problems to be solved:
* Synonyms, like "SVM" and "Support Vector Machine",  "Clustering", "Clustering Algorithm" 
* hypernyms, like "Text Categorization" and "Academic Text Categorization".

Methods to solve these problems.

### Prediction
---------------
Given a problem, predicting new problem and solution pair will be applied in future is a link prediction problem. Methods in following:
* Similarity based: Common neighbors, Jaccard, Adar.
* Low Rank Approximation: SVD.
* Graph based: Rand Walk.
* Supervised: Binary classification of a link.

Thanks to work of [clarkkev](https://github.com/clarkkev/bipartite-link-prediction/blob/master/similarity.py), we mainly used these four kinds of commonly used link prediction methods.











	
