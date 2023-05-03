# This programme reads one company's raw data and outputs one final data file.
# Each company has 4 raw data files, from bloomberg, cnbc, wsj, and yahoo.
# You only need to indicate the company name at the very start.
# Valid inputs: "apple", "tesla", "google", "amazon", "microsoft", "nvidia".

import pandas as pd
import numpy as np

# indicate company name
name = input("Please input the company name:\n").lower()

# read raw data to DataFrames
bb = pd.read_excel(name + "_bloomberg.xlsx")
cb = pd.read_excel(name + "_cnbc.xlsx")
ws = pd.read_excel(name + "_wsj.xlsx")
yh = pd.read_excel(name + "_yahoo.xlsx")



# processing Bloomberg data

# drop unnamed & irrelevant columns, reorder columns
bb = bb.drop(columns = [col for col in bb.columns if 'Unnamed' in col])
bb = bb.drop(columns = ['detailLink', 'authors'])
bb = bb[['date', 'title', 'summary']]

# drop duplicated rows, rows with N/A or invalid entries
bb = bb.drop_duplicates()
bb = bb.dropna()
invalid_date_mask = pd.to_datetime(bb['date'], errors = 'coerce').isna()
bb = bb[~invalid_date_mask]
bb = bb.loc[bb['title'].apply(lambda x: isinstance(x, str))].dropna()
bb = bb.loc[bb['summary'].apply(lambda x: isinstance(x, str))].dropna()
invalid_summary_mask = bb['summary'].str.contains('https?://')
bb = bb[~invalid_summary_mask]

# replace special characters in columns 'title' & 'summary'
bb['title'] = bb['title'].str.replace('‚Äì', ',')
bb['title'] = bb['title'].str.replace('‚Äî', ',')
bb['title'] = bb['title'].str.replace('‚Äò', '')
bb['title'] = bb['title'].str.replace('‚Äô', "'")
bb['title'] = bb['title'].str.replace('‚Äú', '')
bb['title'] = bb['title'].str.replace('‚Äù', '')
bb['title'] = bb['title'].str.replace('‚Ä¶', '.')
bb['title'] = bb['title'].str.replace('\.\.\.', '.')
bb['title'] = bb['title'].str.replace('‚Ä\?', '')
bb['title'] = bb['title'].str.replace('‚Ä¢', '')
bb['title'] = bb['title'].str.replace('¬Æ', '')
bb['summary'] = bb['summary'].str.replace('‚Äì', ',')
bb['summary'] = bb['summary'].str.replace('‚Äî', ',')
bb['summary'] = bb['summary'].str.replace('‚Äò', '')
bb['summary'] = bb['summary'].str.replace('‚Äô', "'")
bb['summary'] = bb['summary'].str.replace('‚Äú', '')
bb['summary'] = bb['summary'].str.replace('‚Äù', '')
bb['summary'] = bb['summary'].str.replace('‚Ä¶', '.')
bb['summary'] = bb['summary'].str.replace('\.\.\.', '.')
bb['summary'] = bb['summary'].str.replace('‚Ä\?', '')
bb['summary'] = bb['summary'].str.replace('‚Ä¢', '')
bb['summary'] = bb['summary'].str.replace('¬Æ', '')

# drop rows containing non-Ascii characters, considering 'title' & 'summary'
bb = bb[bb['title'].apply(lambda x: x.isascii())]
bb = bb[bb['summary'].apply(lambda x: x.isascii())]

# format date column, and keep date information only
bb['date'] = pd.to_datetime(bb['date'])
bb['date'] = [time.date() for time in bb['date']]

# check duplicated rows, rows with N/A, again, and reset row index
bb = bb.drop_duplicates()
bb = bb.dropna()
bb.reset_index(drop = True, inplace = True)



# processing CNBC data

# drop unnamed & irrelevant columns, reorder columns
cb = cb.drop(columns = [col for col in cb.columns if 'Unnamed' in col])
cb = cb.drop(columns = ['link', 'section', 'content'])
cb = cb[['date', 'title', 'summary']]

# drop duplicated rows, rows with N/A or invalid entries
cb = cb.drop_duplicates()
cb = cb.dropna()
invalid_date_mask = pd.to_datetime(cb['date'], errors = 'coerce').isna()
cb = cb[~invalid_date_mask]
cb = cb.loc[cb['title'].apply(lambda x: isinstance(x, str))].dropna()
cb = cb.loc[cb['summary'].apply(lambda x: isinstance(x, str))].dropna()

# replace special characters in columns 'title' & 'summary'
cb['title'] = cb['title'].str.replace('\.\.\.', '.')
cb['summary'] = cb['summary'].str.replace('\.\.\.', '.')

# drop rows containing non-Ascii characters, considering 'title' & 'summary'
cb = cb[cb['title'].apply(lambda x: x.isascii())]
cb = cb[cb['summary'].apply(lambda x: x.isascii())]

# format date column, and keep date information only
cb['date'] = pd.to_datetime(cb['date'])
cb['date'] = [time.date() for time in cb['date']]

# check duplicated rows, rows with N/A, again, and reset row index
cb = cb.drop_duplicates()
cb = cb.dropna()
cb.reset_index(drop = True, inplace = True)



# processing WSJ data

# drop unnamed & irrelevant columns, reorder columns
ws = ws.drop(columns = [col for col in ws.columns if 'Unnamed' in col])
ws = ws.drop(columns = 'link')
ws = ws[['date', 'title', 'summary']]

# drop duplicated rows, rows with N/A or invalid entries
ws = ws.drop_duplicates()
ws = ws.dropna()
invalid_date_mask = pd.to_datetime(ws['date'], errors = 'coerce').isna()
ws = ws[~invalid_date_mask]
ws = ws.loc[ws['title'].apply(lambda x: isinstance(x, str))].dropna()
ws = ws.loc[ws['summary'].apply(lambda x: isinstance(x, str))].dropna()

# replace special characters in columns 'title' & 'summary'
ws['title'] = ws['title'].str.replace('\.\.\.', '.')
ws['summary'] = ws['summary'].str.replace('\.\.\.', '.')

# drop rows containing non-Ascii characters, considering 'title' & 'summary'
ws = ws[ws['title'].apply(lambda x: x.isascii())]
ws = ws[ws['summary'].apply(lambda x: x.isascii())]

# format date column, and keep date information only
ws['date'] = pd.to_datetime(ws['date'])
ws['date'] = [time.date() for time in ws['date']]

# check duplicated rows, rows with N/A again, and reset row index
ws = ws.drop_duplicates()
ws = ws.dropna()
ws.reset_index(drop = True, inplace = True)



# processing Yahoo data

# drop unnamed & irrelevant columns, rename and reorder columns
yh = yh.drop(columns = [col for col in yh.columns if 'Unnamed' in col])
yh = yh.drop(columns = ['Source', 'Link', 'Content'])
yh = yh.rename(columns = {'Title': 'title',
                          'Date': 'date',
                          'Description': 'summary'})
yh = yh[['date', 'title', 'summary']]

# drop duplicated rows, rows with N/A or invalid entries
yh = yh.drop_duplicates()
yh = yh.dropna()
invalid_date_mask = pd.to_datetime(yh['date'], errors = 'coerce').isna()
yh = yh[~invalid_date_mask]
yh = yh.loc[yh['title'].apply(lambda x: isinstance(x, str))].dropna()
yh = yh.loc[yh['summary'].apply(lambda x: isinstance(x, str))].dropna()

# replace special characters in columns 'title' & 'summary'
yh['title'] = yh['title'].str.replace('‚Äì', ',')
yh['title'] = yh['title'].str.replace('‚Äî', ',')
yh['title'] = yh['title'].str.replace('‚Äò', '')
yh['title'] = yh['title'].str.replace('‚Äô', "'")
yh['title'] = yh['title'].str.replace('‚Äú', '')
yh['title'] = yh['title'].str.replace('‚Äù', '')
yh['title'] = yh['title'].str.replace('‚Ä¶', '.')
yh['title'] = yh['title'].str.replace('\.\.\.', '.')
yh['title'] = yh['title'].str.replace('‚Ä\?', '')
yh['title'] = yh['title'].str.replace('‚Ä¢', '')
yh['title'] = yh['title'].str.replace('¬Æ', '')
yh['summary'] = yh['summary'].str.replace('‚Äì', ',')
yh['summary'] = yh['summary'].str.replace('‚Äî', ',')
yh['summary'] = yh['summary'].str.replace('‚Äò', '')
yh['summary'] = yh['summary'].str.replace('‚Äô', "'")
yh['summary'] = yh['summary'].str.replace('‚Äú', '')
yh['summary'] = yh['summary'].str.replace('‚Äù', '')
yh['summary'] = yh['summary'].str.replace('‚Ä¶', '.')
yh['summary'] = yh['summary'].str.replace('\.\.\.', '.')
yh['summary'] = yh['summary'].str.replace('‚Ä\?', '')
yh['summary'] = yh['summary'].str.replace('‚Ä¢', '')
yh['summary'] = yh['summary'].str.replace('¬Æ', '')

# drop rows containing non-Ascii characters, considering 'title' & 'summary'
yh = yh[yh['title'].apply(lambda x: x.isascii())]
yh = yh[yh['summary'].apply(lambda x: x.isascii())]

# format date column, and keep date information only
yh['date'] = pd.to_datetime(yh['date'])
yh['date'] = [time.date() for time in yh['date']]

# check duplicated rows, rows with N/A, again, and reset row index
yh = yh.drop_duplicates()
yh = yh.dropna()
yh.reset_index(drop = True, inplace = True)



# merging stage

# concatenate the 4 cleaned datasets
df = pd.concat([bb, cb, ws, yh], ignore_index = True)

# add the 'platform' column with source platform information
df['platform'] = np.where(df.index < len(bb), 'bloomberg', 
                          np.where(df.index < len(bb) + len(cb), 'cnbc',
                                   np.where(df.index < len(bb) + len(cb) + len(ws), 'wsj', 'yahoo')))

# reorder columns
df = df[['date', 'platform', 'title', 'summary']]

# sort by date (newest to oldest)
df = df.sort_values(by = 'date', ascending = False)

# keep rows with date in this range: 2020-07-04 to 2023-04-17 (inclusive)
df = df[(df['date'] >= pd.to_datetime('2020-07-04').date()) &
        (df['date'] <= pd.to_datetime('2023-04-17').date())]

# export the merged file
df.to_excel(name + '.xlsx', index = False)