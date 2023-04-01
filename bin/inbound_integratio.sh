#!/bin/bash
source /home/frontend/anaconda3/etc/profile.d/conda.sh
conda activate accountant_env # change to your conda environment's name
# -u: unbuffered output
uvicorn inbound:app --reload --host 127.0.0.1 --port 8500 --workers 4
