#coding:utf-8
import sys
from collections import defaultdict
import json
sys.path.append(".")
from util import *
reload(sys)
sys.setdefaultencoding('utf-8')

def export_from_database():
	import MySQLdb
	db = MySQLdb.connect("localhost","root","hy123","ACM_QM")
	cursor = db.cursor()
	sql = "select acm_paper.title, acm_paper.year, acm_paper.authorID, acm_paper.titlechunk, pattern_acm_title_chunk.pattern from ACM_QM.acm_paper, ACM_QM.pattern_acm_title_chunk, ACM_QM.pattern_title_pattern where pattern_title_pattern.paperID = acm_paper.id and pattern_title_pattern.patternID = pattern_acm_title_chunk.id"
	cursor.execute(sql)
	logger = iters_logger(10000,"count acm papers")
	acm_papers = defaultdict(dict)
	results = cursor.fetchall()
	for row in results:
		title = row[0]
		year = row[1]
		title_chunk = row[3]
		pattern = row[4]

		paper = {}
		paper['title']=title.decode("ISO-8859-1").encode('utf-8')
		paper['year'] = str(year)
		paper['title_chunk'] = title_chunk.replace("\t","==").decode("ISO-8859-1").encode('utf-8')
		paper['pattern'] = pattern.decode("ISO-8859-1").encode('utf-8')
		ID = title+"==="+str(year)
		ID=ID.decode("ISO-8859-1").encode('utf-8')
		logger.step()
		acm_papers[ID]=paper

	logger.end()
	print json.dumps(acm_papers)




# #extract titles with specific patterns
# def paper_within_patterns(paper_file_path,pattern_file_path):

# 	patternset = set([ p.strip() for p in open(pattern_file_path)])

# 	count = {} 
# 	for line in open(paper_file_path):
# 		pattern = line.strip().split("====")[-1]
# 		if pattern in patternset:
# 			#count[pattern] = count.get(pattern,0)+1		
# 			print line.strip()



def extract_acm_articles():
	import MySQLdb
	db = MySQLdb.connect("localhost","root","hy123","ACM_PAPER")
	cursor = db.cursor()
	sql = "select acm_article.article_id, acm_article.art_pub_year, acm_article.Acm_Article_Title, acm_article.Acm_Article_Abstract, Acm_Author_Ids, art_au_text, art_inst_id, art_inst_text from acm_article"
	cursor.execute(sql)
	results = cursor.fetchall()

	acm_papers = defaultdict(list)
	logger = iters_logger(10000,"counting acm articles")
	for row in results:

		article_id = row[0]
		year = row[1]
		title = row[2]
		abstext = row[3]
		auIds = row[4]
		aus = row[5]
		instids = row[6]
		insts = row[7]

		#filter out the articles without abstract
		if "An abstract is not available." in abstext:
			continue

		ID = title+"==="+str(year)
		ID = ID.decode("ISO-8859-1").encode('utf-8')
		paper= {}
		paper['id'] = str(article_id)
		paper['year']=str(year)
		paper['title']=title.decode("ISO-8859-1").encode('utf-8')
		paper['abstract'] = abstext.decode("ISO-8859-1").encode('utf-8')
		paper['auIds'] = auIds
		paper['aus'] = aus.decode("ISO-8859-1").encode('utf-8')
		paper['instids'] = instids
		paper['insts'] = insts.decode("ISO-8859-1").encode('utf-8')
		logger.step()

		acm_papers[ID] = paper

	logger.end()
	paper_str = json.dumps(acm_papers)
	print unicode(paper_str, errors="ignore")


# match two databases
def match_two_databases(acm_paper,acm_article):
	acm_papers = json.loads(open(acm_paper).readline().strip())
	acm_articles = json.loads(open(acm_article).readline().strip())

	articles_keyset = set(acm_articles.keys())

	logger  = iters_logger(10000,"matching two databases")
	new_articles = defaultdict(dict)
	for key in acm_papers.keys():
		if key in articles_keyset:

			paper={}
			paper['id'] = acm_articles[key]['id']
			paper['year']=acm_articles[key]['year']
			paper['title']=acm_articles[key]['title']
			paper['abstract'] = acm_articles[key]['abstract']
			paper['auIds'] = acm_articles[key]['auIds']
			paper['aus'] = acm_articles[key]['aus']
			paper['instids'] = acm_articles[key]['instids']
			paper['insts'] = acm_articles[key]['insts']
			paper['title_chunk'] = acm_papers[key]['title_chunk']
			paper['pattern'] = acm_papers[key]['pattern']

			new_articles[acm_articles[key]['id']] = paper
			logger.step()

	logger.end()
	print json.dumps(new_articles) 


# def combine_patterns_and_acm_articles(patterns,acm_articles):
# 	titleset = set([])
# 	pattern_dic={}
# 	for line in open(patterns):
# 		line=line.strip()
# 		splits = line.split("====")
# 		titleset.add("==".join(line.strip().split("====")[:2]))
# 		pattern_dic["==".join(line.strip().split("====")[:2])] = line


# 	for line in open(acm_articles):
# 		line=line.strip()
# 		splits = line.split("====")
# 		pid = splits[2]+"=="+splits[1]
# 		if pid in titleset:
# 			print pattern_dic[pid]+"===="+"====".join(splits)


op = sys.argv[1]
if op == "gen_acm_article":
	extract_acm_articles()
elif op == "extract_pattern_paper":
	export_from_database()
elif op == "match":
	match_two_databases(sys.argv[2],sys.argv[3])
else:
	sys.stderr.write("No such operations!\n")









