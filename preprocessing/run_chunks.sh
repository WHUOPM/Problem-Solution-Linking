
echo ""

echo "RUN chunk parsing...."
folder_path=/Users/huangyong/pyspace/Problem-Solution-Linking/data
index_path=index_el.txt
start=0
end=10
worker=2
python preprocessing/patterns_generation.py chunk_folder ${folder_path} ${index_path} ${start} ${end} ${worker}