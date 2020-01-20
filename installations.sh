cd fastText-master/
make
pip install .
cd ..
pip install spacy
python -m spacy download en_core_web_sm
pip install -r requirements.txt