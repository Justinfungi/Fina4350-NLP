import sys 
sys.path.append("..") 

from finbert.finbert import predict
import argparse
import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
parser = argparse.ArgumentParser(description='Sentiment analyzer')

parser.add_argument('-a', action="store_true", default=False)
parser.add_argument('--table_path', type=str, help='Path to the dataset table.')
parser.add_argument('--output_dir', type=str, help='Where to write the results')
parser.add_argument('--model_path', type=str, help='Path to classifier model')

args = parser.parse_args()

if not os.path.exists(args.output_dir):
    os.mkdir(args.output_dir)

model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
head, tail = os.path.split(args.table_path)
output = "predictions_"+tail[:-4]+"csv"
print("output stored in: ", os.path.join(args.output_dir,output))

def store(dict, date, score_title, score_summary):
    dict["date"].append(date)
    dict["score_title"].append(score_title)
    dict["score_summary"].append(score_summary)

###############################################

# initialize
df = pd.read_excel(args.table_path)
# df = df.sort_values(by=['date', 'platform'])
last_date = df["date"][0]
cul_score_title, cul_score_summary, counter = 0, 0, 0
output_dict = {"date": [],
               "score_title": [],
               "score_summary": []}

length = len(df)
# length = 10 # for debug testing

for i in range(length):
    date, platform, title, summary = df["date"][i], df["platform"][i], df["title"][i], df["summary"][i]
    
    # store if comes to a new day
    if ((last_date) != (date)):
        store(output_dict, last_date, cul_score_title/counter, cul_score_summary/counter)
        # initialize again
        cul_score_title, cul_score_summary, counter = 0, 0, 0
    
    # get score for the new title and summary
    score_title = predict(title, model, write_to_csv=False)
    cul_score_title += score_title
    score_summary = predict(summary, model, write_to_csv=False)
    cul_score_summary += score_summary
    counter += 1
    last_date = date

    # showing progress
    if i % 100 == 0:
        print("finish", i, "/", length)

store(output_dict, last_date, cul_score_title/counter, cul_score_summary/counter)
df_out = pd.DataFrame.from_dict(output_dict)
print(df_out)
df_out.to_csv(os.path.join(args.output_dir,output))
