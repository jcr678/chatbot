conda create --name project python=3.6
conda activate project
pip install -r requirements.txt
python -m spacy download en #if you're on windows you may have to run this on administrator mode. en should link before moving on.
python merged.py
