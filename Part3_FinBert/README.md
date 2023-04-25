# How to use in our project:
requirements
```
nltk
tqdm
transformers
```

To get the sentence_level and average sentiment score of one text, enter `scripts` and run:
```
python scripts/predict_dataset.py --table_path {TABLE_PATH} --output_dir {OUTPUT_FOLDER_PATH} --model_path models/classifier_model/finbert-sentiment
<!-- python predict_dataset.py --output_dir ../output/ --model_path models/classifier_model/finbert-sentiment --table_path ../data/microsoft.xlsx -->
```


The model will be downloaded directly during the first running time. So no need to download by yourself.

Data available for next stage:
amazon
apple
google
microsoft ❌
nvidia
tesla