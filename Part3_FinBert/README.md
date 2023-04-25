# How to use in our project:
## Requirements
```
nltk
tqdm
transformers
```
## Running
To get the sentence_level and average sentiment score of one text, enter `scripts` and run:
```
python scripts/predict_dataset.py \
    --output_dir {OUTPUT_FOLDER_PATH} \
    --model_path models/classifier_model/finbert-sentiment \
    --table_path {INPUT_TABLE_ADDRESS} \
    --mode { check / run }
```
The **check** mode is to check if there's invalid textual data inside the table. It can finish running in minutes. 

The **run** mode is for converting the textual data into the average sentiment scores of each title / paragraph of summary. The output core is in [-1, 1], where a negative value means a bad comment. 

The model will be downloaded directly during the first running time. So no need to download by yourself.

## Data processing for next stage
| Company | Progress|
| ------- | ------- |
| Amazon  |  Done!  |
|  Apple  |  Done!  |
| Google  |  Done!  |
|Microsoft|  Done!  |
| Nvidia  |  Done!  |
|  Tesla  |  Done!  |

All the prediction scores are in csv files inside `output/` folder. 

## Data format
1. **Input data**: One `{company}.xlsx` file for each company in `data/`. Dataframe structure and example shows as follows:

| date | plarform | title | summary |
|--|--|--|--|
| 2023-04-17 | bloomberg | Transcript: So ... in Reverse | Over time ... exclude East Asia. |

2. **Output data**: One `predictions_{company}.csv` file for each company in `output/`. Dataframe structure and example shows as follows: 

|  | date | score_title | score_summary |
|---|---|---|---|
| 0 | 2023-04-17 | -0.050246828546126686 | -0.060826936115821205 |

