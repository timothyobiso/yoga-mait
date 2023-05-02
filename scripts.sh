# LOADING THE POSES INDEX

# 1. In powershell, direct to the elasticsearch folder
# 2. Run "./bin/elasticsearch"
# 3. Load pretrained sentence BERT encoder. Each embedding has 768 dimensions
python -m embedding_service.server --embedding sbert  --model all-mpnet-base-v2
# 4. Load poses into the index called "poses"
python load_index.py --index_name poses --poses_folder_path data