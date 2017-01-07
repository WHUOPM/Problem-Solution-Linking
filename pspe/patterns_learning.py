#coding:utf-8
import sys
import json
from collections import defaultdict
sys.path.append(".")
from util import *
import math

def match_patterns(dic):
	patterns = dic['pattern'].split()
	title_chunks = dic['title_chunk'].split("==")

	problem=None
	solution=None
	if len(patterns)!= len(title_chunks):
		return problem,solution

	if dic['pattern']=="NP using NP":
		solution = title_chunks[2].split(":")[0]
		problem = title_chunks[0].split(":")[0]
	elif dic['pattern']=="NP based on NP":
		solution = title_chunks[3].split(":")[0]
		problem = title_chunks[0].split(":")[0]


	return problem,solution

#generate seeds using pattern 'NN using NN'
#saved to data/problems.json and data/solutions.json
def generate_seeds(acm_conf_json):
	acm_conf_articles = json.loads(open(acm_conf_json).read().strip())

	logger = iters_logger(1000,"generating seeds")
	seeddict = defaultdict(list)
	for ids in acm_conf_articles.keys():
		dic = acm_conf_articles[ids]
		problem,solution = match_patterns(dic)
		if problem and solution:
			# a entity could be problem in a paper, but be solution in others
			# so, seed entities should match the files 
			seeddict['problem'].append(problem.lower())
			seeddict['solution'].append(solution.lower())
			logger.step()

	open("data/seeds.json","w").write(json.dumps(seeddict))
	logger.info("saved to data/seeds.json")
	logger.end()


#extract trips from reverb result
def reverb_pattern_extraction():
	pattern_dic = defaultdict(list)
	logger = iters_logger(10000,"extract patterns")
	entities_set=set()
	pattern_set = set()
	for line in open("data/bak/reverb_result.txt"):
		splits= line.strip().split("\t")
		if len(splits)!=18:
			continue
		#ids = splits[0].split("_")[-3]
		#trips 
		arg1,relation,arg2 = splits[15].decode("ISO-8859-1").encode('utf-8'),splits[16].decode("ISO-8859-1").encode('utf-8'),splits[17].decode("ISO-8859-1").encode('utf-8')

		pattern_dic[arg1].append("NN=="+relation)
		pattern_dic[arg2].append(relation+ "==NN")
		entities_set.add(arg1)
		entities_set.add(arg2)

		pattern_dic["NN=="+relation].append(arg1)
		pattern_dic[relation+ "==NN"].append(arg2)
		pattern_set.add("NN=="+relation)
		pattern_set.add(relation+ "==NN")

		logger.step()

	logger.info("{:} entities and {:} patterns are extracted".format(len(entities_set),len(pattern_set)))	
	logger.end()


	open("data/reverb_patterns.json","w").write(json.dumps(pattern_dic))


def score_patterns(patternlist,reverb_patterns,entities):
	#using RLOGF = (F/N)*log(F)
	#F is the number pattern extracted in entities, N is total number
	pattern_dic={}
	es= set(entities)
	for pattern in set(patternlist):
		all_entites = reverb_patterns[pattern]
		F = len(all_entites & es)
		#sys.stderr.write("patterns extracted size: {:}\n".format(F))

		RlogF = (float(F)/len(all_entites))*math.log(F)
		pattern_dic[pattern] = RlogF


	return sorted(pattern_dic.items(),key=lambda x:x[1], reverse = True)




#entities -> patterns
def entities_to_patterns(logger,entities,patterns,reverb_patterns, \
	max_patterns_learned_per_iter=100, \
	min_score_of_patterns=0.1,min_number_of_patterns=1):

	logger.info("number of entities begin: {:}".format(len(entities)))
	patternlist = []
	for entity in entities:
		pl = reverb_patterns.get(entity.lower(),None)
		if pl is not None:
			patternlist.extend([p for p in pl if len(reverb_patterns[p])>min_number_of_patterns])
	
	logger.info("candidate pattern list size: {:}".format(len(set(patternlist))))

	count = 0 
	for (k,v) in score_patterns(patternlist,reverb_patterns,entities):
		if count >= max_patterns_learned_per_iter:
			break

		if k not in patterns and v> min_score_of_patterns:
			count += 1
			patterns.append(k)

	logger.info("number of new patterns: {:}".format(count))

	return patterns

#patterns -> entities
# selected patterns extract correct entities
def patterns_to_entities(logger,entities,patterns,reverb_patterns,max_entities_learned_per_iter=10, min_number_of_patterns=1):
	
	entitieslist = []
	for pattern in patterns:
		entitieslist.extend(reverb_patterns[pattern])

	entitieslist=set(entitieslist)
			
	logger.info("found {:} candidate entities".format(len(entitieslist)))

	ps = set(patterns)
	new_entities={}
	for entity in entitieslist:
		new_entities[entity] = len(reverb_patterns[entity] &  ps)


	

	count = 0
	for (k,v) in sorted(new_entities.items(),key=lambda x:x[1], reverse = True):

		if count >= max_entities_learned_per_iter:
			break

		if k not in entities and v > min_number_of_patterns:
			count+=1
			entities.append(k)

	logger.info("number of new entities: {:}".format(count))

	return entities


	

def one_step(ps_entities,ps_patterns,reverb_patterns,logger, \
	max_patterns_learned_per_iter=100, max_entities_learned_per_iter=10, \
	min_score_of_patterns=0.1, min_number_of_patterns=10):
	""" one step in bootstrapping"""
	
	problem_patterns,solution_patterns = ps_patterns['problem'],ps_patterns['solution']
	problem_entities,solution_entities = ps_entities['problem'],ps_entities['solution']
	#from entities to patterns
	logger.info("problem entities -> problem patterns")
	problem_patterns = entities_to_patterns(logger,problem_entities,problem_patterns,reverb_patterns,max_patterns_learned_per_iter,min_score_of_patterns,min_number_of_patterns)
	logger.info("solution entities -> solution patterns")
	solution_patterns = entities_to_patterns(logger,solution_entities,solution_patterns,reverb_patterns,max_patterns_learned_per_iter,min_score_of_patterns,min_number_of_patterns)

	# from patterns to entities
	logger.info("problem patterns -> problem entities")
	problem_entities = patterns_to_entities(logger,problem_entities,problem_patterns,reverb_patterns,max_entities_learned_per_iter,min_number_of_patterns)
	logger.info("solution patterns -> solution entities")
	solution_entities = patterns_to_entities(logger,solution_entities,solution_patterns,reverb_patterns,max_entities_learned_per_iter,min_number_of_patterns)

	ps_entities['problem'] = problem_entities
	ps_entities['solution'] = solution_entities
	ps_patterns['problem'] = problem_patterns
	ps_patterns['solution'] = solution_patterns
	logger.info("iteration complete!")
	logger.info("learned {:} problem entities and {:} problem patterns".format(len(problem_entities),len(problem_patterns)))
	logger.info("learned {:} solution entities and {:} solution patterns".format(len(solution_entities),len(solution_patterns)))
	return ps_entities,ps_patterns


def bootstraped_learning(seeds_json,reverb_patterns_json, \
	n_iters=100, max_patterns_learned_per_iter=500, max_entities_learned_per_iter=100, \
	min_score_of_patterns=0.1, min_number_of_patterns = 1, save_step=1):
	
	logger  = iters_logger(1,"iteratively learning entities and patterns for {:} iters".format(n_iters))
	logger.info("loading seeds and data...")
	seeds_dict = json.loads(open(seeds_json).read().strip())
	reverb_patterns = json.loads(open(reverb_patterns_json).read().strip())

	for key in reverb_patterns.keys():
		reverb_patterns[key] = set(reverb_patterns[key])


	logger.info("loading complete!")
	logger.info("Initial size of seeds, problems: {:} and solutions: {:}".format(len(seeds_dict['problem']),len(seeds_dict['solution'])))
	logger.info("Entities and Patterns pre-extracted: {:}".format(len(reverb_patterns)))
	#logger.info("Initial size of problem dict and solution dict is {:} and {:}".format(len(problemdic)))
	#ps_patterns{'problem':[],"solution":[]}
	ps_patterns = defaultdict(list)
	for i in range(n_iters):
		logger.step()

		#pre_dict size 

		seeds_dict, ps_patterns = one_step(seeds_dict,ps_patterns,\
			reverb_patterns,logger,max_patterns_learned_per_iter=max_patterns_learned_per_iter, max_entities_learned_per_iter=max_entities_learned_per_iter, \
			min_score_of_patterns=min_score_of_patterns,min_number_of_patterns=min_number_of_patterns)

		if (i+1) %save_step==0:
			logger.info("Iter {:}, save entities to data/seeds.json, patterns to data/patterns.json".format(i+1))
			#saved the result
			open("data/seeds.json","w").write(json.dumps(seeds_dict))
			open("data/patterns.json","w").write(json.dumps(ps_patterns))

	logger.info("bootstrap's done!")
	logger.info("learned {:} problem entities and {:} problem patterns".format(len(seeds_dict['problem']),len(ps_patterns['problem'])))
	logger.info("learned {:} solution entities and {:} solution patterns".format(len(seeds_dict['solution']),len(ps_patterns['solution'])))



op = sys.argv[1]
if op == "gen_seeds":
	generate_seeds(sys.argv[2])
elif op == "extract_patterns":
	reverb_pattern_extraction()
elif op == "bootstrap":
	bootstraped_learning(sys.argv[2],sys.argv[3])







