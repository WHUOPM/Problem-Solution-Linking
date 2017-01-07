import sys
sys.path.append(".")
from util import *
import json
from collections import defaultdict

def all_possible_entities(pattern_dict_json, learned_patterns):
	
	logger = iters_logger(1000,"Extraction of problem and solution entities based on learned patterns")
	pattern_dict = json.loads(open(pattern_dict_json).read().strip())
	learned_patterns = json.loads(open(learned_patterns).read().strip())

	logger.info("starting extraction of problem entities.")
	count=0
	problem_entities = defaultdict(list)
	#problem patterns
	for pattern in learned_patterns['problem']:
		for entity in pattern_dict[pattern].keys():
			for ids in pattern_dict[pattern][entity]:
				problem_entities[ids].append(entity) 
				count+=1

	logger.info("{:} problem entities are found.".format(count))
	open("data/problem_entities.json","w").write(json.dumps(problem_entities))


	count=0
	logger.info("starting extraction of solution entities.")
	solution_entities = defaultdict(list)
	for pattern in learned_patterns['solution']:
		for entity in pattern_dict[pattern].keys():
			for ids in pattern_dict[pattern][entity]:
				solution_entities[ids].append(entity)
				count+=1

	logger.info("{:} solution entities are found.".format(count))
	logger.end()
	open("data/solution_entities.json","w").write(json.dumps(solution_entities))


op = sys.argv[1]
if op=="ape":
	all_possible_entities(sys.argv[2],sys.argv[3])






