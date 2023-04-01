#!/bin/bash
source /home/frontend/anaconda3/etc/profile.d/conda.sh
conda activate accountantnlu_env # change to your conda environment's name
# -u: unbuffered output
uvicorn app:app --reload --host 0.0.0.0 --port 5400 --workers 4
