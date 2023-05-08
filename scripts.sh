# INSTRUCTIONS ON LOADING THE POSES INDEX
# Developed by Anastasiia Tatlubaeva

# 1. In powershell, direct to the elasticsearch folder.
# 2. Run "./bin/elasticsearch".
# 3. Load pretrained sentence BERT encoder. Each embedding has 768 dimensions,
#    Run the code below in a terminal.
#    Make sure it runs in the background while using the application.
python -m embedding_service.server --embedding sbert --model all-mpnet-base-v2
# 4. Load poses into the index called "poses".
#    Run the code below in a separate terminal.
#    Make sure it runs in the background while using the application
python load_index.py --index_name poses --poses_folder_path data