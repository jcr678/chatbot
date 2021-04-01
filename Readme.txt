conda create --name project python=3.6
conda activate project
python -m spacy download en
pip install -r requirements.txt
python merged.py
