# echo "extracting problem solution pairs from articles."

# echo ""

# echo "extract pattern from reverb result and saved to data/reverb.json"
# python psps_extraction/problem_solution_pairs_extraction.py extract_patterns
# # result: entities 1270145 patterns 244006


echo " "

echo "generate seeds using pattern 'NN using NN' and 'NN based on NN' from titles"]
python psps_extraction/problem_solution_pairs_extraction.py gen_seeds data/acm_conf_articles.json


echo ""
echo "bootstrapped learning patterns and entities"
seedsjson=data/seeds.json
reverbpattern=data/reverb_patterns.json
python psps_extraction/problem_solution_pairs_extraction.py bootstrap ${seedsjson}  ${reverbpattern} 




echo "DONE"