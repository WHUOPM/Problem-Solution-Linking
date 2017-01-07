

# echo "extracting problem solution pairs from articles."

# echo ""

# echo "extract pattern from reverb result and saved to data/reverb_patterns.json"
# python pspe/patterns_learning.py extract_patterns
# # result: entities 1270145 patterns 244006

# echo "extract all patterns"

# python pspe/patterns_learning.py pattern_dict


echo " "

echo "generate seeds using pattern 'NN using NN' and 'NN based on NN' from titles"]
python pspe/patterns_learning.py gen_seeds data/acm_conf_articles.json


echo ""
echo "bootstrapped learning patterns and entities"
seedsjson=data/seeds.json
reverbpattern=data/reverb_patterns.json
python pspe/patterns_learning.py bootstrap ${seedsjson}  ${reverbpattern} 


echo "DONE"