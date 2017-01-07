## Problem and Solution Pairs Extraction (PSPE)
Codes for representing papers' as problem and solution pairs. Three steps are implemented:
1. Patterns learning: Applying a bootstrapping methods to learn problem patterns and solution patterns. --> patterns_learning.py
2. Extracting all possible problem entities and solution entities from papers' abstract.
3. Two binary classifier will be trained to identify a paper's main problem entity and solution entity from all problem entities and solution entities of that paper.