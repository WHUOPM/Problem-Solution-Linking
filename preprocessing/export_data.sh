 
#==== export data from database ====

echo "processing starting ...."
echo ""
echo 'export  acm articles from database ACM_PAPER'
python preprocessing/DataExporter.py gen_acm_article > data/acm_articles.json

echo "export  acm paper from acm_QM of qikai's processing "
python preprocessing/DataExporter.py extract_pattern_paper > data/acm_papers.json

#match two databases
echo "match two database"
python preprocessing/DataExporter.py match data/acm_papers.json data/acm_articles.json > data/acm_conf_articles.json

echo ""
echo "DONE"

#======data generator for entity learning ====

# generate files used to entities learning
#----
# echo "generate files for entities learning"
#python preprocessing/datafactory.py gen_el_files data/acm_articles.txt 
#----

# extract problem and solution entities
#----
#python preprocessing/datafactory.py gen_ps_entities data/combine.txt > data/ps_entities.txt
#----


# generate seeds for entity learning
#----
#python preprocessing/datafactory.py gen_seeds data/ps_entities.txt
#----
