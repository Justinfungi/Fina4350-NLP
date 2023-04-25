**GROUP 6 EveGPT**

# Blog 1 - Bag of Word
Author: Fung Ho Kit  
Co-Author: Yang Fan, Zhu Jiarui, Li Xinran  
Created date: 2023.02.05  

During the lecture, Dr.BUEHLMAIER showed us the spying program for Twitter. The program catches my message and downloads it on the laptop. While the program can capture the tweets containing words that are specified in a word bank, a question appeared in my mind - What kind of words should I monitor?

I think the situations should be complicated given the complex operations in the financial markets. By applying the divide-and-conquer method, a categorization should work well to better classify the various need in different situations

From my point of view, a possible way to categorize is that we divided the whole pie into:

- i) Capital markets (bond, equity securities, derivative securities);
- iv) Cryptocurrency markets

The reasons for my division are:

- i) The first one is the knowledge I obtained from the course [FINA2320] and [FINA2330], I think that there are different focuses in these different markets, and a separation of word bank increase the possibility that we can scrape useful information. For example, the stock markets should focus on the companies' behaviors. Once we fix the portfolio of stocks, we can closely monitor the tweet related to those companies' operations, such as a large cash flow or some agency problem that occurred.

- ii) The second one is the learning I gained from my current internship experience [Optymize Potocol @Optymize_xyz]. I noticed that it is an increasing new market in web3. The behaviors of the market are greatly different from those of traditional markets. More attention should be put on the scam issue, the extent of success in building the community, and so on.

- iii) I do not add the money market into the word banks. It is because the money markets feature in short YTM (year to maturity) and higher opportunity costs. The money market often yields just 2% or 3% while common stocks have returned about 8% to 10% on average. Although the money market owns the advantages of liquidity, monitoring this market is against the initial purpose of this project, which is to create text analytics for better investment strategies in a longer time interval. Thus, the money market is filtered out.

Considering these reasons, I think it is practical, necessary, and efficient to set up multiple word banks for different markets to yield high performance in scraping information for financial analytics.

After the separation of markets, work bank construction is rather essential. Here are some initial thoughts on the focus on each markets.

For crypto market, things are more uncertain and usually out of our expectation. From my point of view, we cannot rely on traditional financial insights to analysis the market trend heavily. First of all, we should focus on the bear market and bull market discussion. The general environment usually are the consequences of multiple aspects, such as policies posed on digital assets, new machanism on chain and so on. Monitoring some gaints and OGs on twitter and Analysis on their prediction on the conditions insides the crypto market is very important. It will help us avoid risk in the investment of crypto.


# Blog 2 - Literture review

*Author: Zhu Jiarui*

*Co-Author: Fung Ho Kit, Yang Fan, Li Xinran*

*Created date: 2023.03.24*

To start our project which aims to generate a framwork which can forecast stock price with historical stock data and realtime forum discussions, we firstly investigated several exsisting works and here are three papers we found might be useful for our project.

## **CNN**: Deep Convolutional Neural Networks for Sentiment Analysis of Short Texts
*Dos Santos, C., & Gatti, M. (2014, August).*

This research conducted by IBM Research proposed **CharSCNN** (Character to Sentence Convolutional Neural Network), uses two convolutional layers to extract relevant features from words and sentences of any size.

1. Initial Representation Levels embeddings

    1. Word-Level Embeddings 

        matrix multiplication

    2. Character-Level Embeddings 

        character-wise CNN

2. Sentence-Level Representation and Scoring

    Produce local features around each word in the sentence and then combines them using a max operation to create a fixed-sized feature vector for the sentence.

Although this paper only conducted polarity analysis and classify the news into positice/negitive only, it generates a unique score for each news and filter it by a certain threshold. We could modify it and keep the score information in our work.


## **BERT**: FinBERT: Financial Sentiment Analysis with Pre-trained Language Models
*Araci, D. (2019).*

Researchers from University of Amsterdam FinBERT proposed a language model based on BERT, to tackle NLP tasks in financial domain. After further trained on 
TRC2-financial and Financial PhraseBank database, FinBERT got outstanding performance on financial news and discussions.


## **LSTM**: Deep learning for stock prediction using numerical and textual information
*Akita, R., Yoshihara, A., Matsubara, T., & Uehara, K. (2016, June).*

This work published on IEEE proposed a novel application of deep learning models, Paragraph Vector, and Long Short-Term Memory (LSTM), to financial time series forecasting. It provides a workable approach for us to combine text information and historical financial data. 

1. Mapping

    Distributed Memory Model of Paragraph Vectors (PV-DM) and Distributed Bag of Words version of Paragraph Vector (PV-DBOW)

2. Financial value converting

    $\Large value_{cn}^t = \frac{2*price_{cn}^t-(max{cn}+min_{cn})}{max_{cn}-min_{cn}}$

After finishing processing the financial and text data individually, the authors utilized the matrix multiplication to unify their vector dimension so that the influence of both data can have similar weights. Then they directly merge the two time sequence of vectors and feed it into LSTM model, so that they wish to forecast the coming stock price. 

# Blog 3 - Scraping Matters

*Author: Yang Fan*

*Co-Author: Fung Ho Kit, Li Xinran, Zhu Jiayi*

*Created date: 2023.04.24*

## What to Scrape
After we had settled on the theme, we decided to scrape on mainstream news media and social media platforms. Considering our selection are all US technology companies, The Wall Street Journal, Consumer News and Business Channel, Bloomberg, and Yahoo News are news media. Social media will focus on Twitter.

## How to Scrape
Web scraping is the process of extracting data from websites using automated tools. It involves sending HTTP requests to websites, retrieving HTML content, and parsing the data to extract relevant information. We use Python and several libraries for our project, including Requests, BeautifulSoup, and Selenium.

### WSJ and CNBC
### Yahoo News
### Bloomberg

## **TWITTER** 
This section is listed separately because Twitter scraping failed.

We first started using Twint for this, and with the workaround in its GitHub Issue, Twint was confirmed to work still. 

（这是一张没有配的插图）

However, after a large number of requests for data, we found that Twint was not officially maintained after the Twitter API was banned, and its "until" function was not working, so we could only read the first ten days of content. Once the request is over ten days, Twint can only retrieve a few tweets, and other people have also mentioned this in issues, but there currently lacks a solution.


# Blog 4 - Data Processing

Author: Li Xinran
Co-Author: Fung Ho Kit, Yang Fan, Zhu Jiarui
Created Date: 2023.04.25

After scraping the text data from various platforms, we need to process it before feeding it into the model. FinBERT supports many common English punctuations and can split a paragraph into sentences by itself. It saved us a lot of work and what we did in the data processing part was mainly cleaning. During cleaning, the main difficulty we ran into was dealing with invalid characters.

At first glance, we noticed that there are some non-English letters (e.g., Ä) in the texts, and we thought: maybe those text entries are in other languages and we should just drop those observations. Once we took a closer look at the data, we found that:

1) Those non-English letters are actually the only "non-English composition" of the text entries where they appear, apart from them, the rest of the text is more or less a valid English paragraph.

2) The appearances of the non-English characters in different text entries show some pattern: certain combinations of those characters appear repetitively (e.g., Äô).

We then guess that those non-English characters were actually punctuations that got messy in the process of scraping. This was proved to be true when we opened the webpage where one of those texts was from.

In this case, we should not simply drop (by filtering out rows with non-Ascii characters) those observations containing invalid characters, because it would be a waste of data. What we did was to look through enough data, and try to find the mappings (e.g., ‚Äô is actually ') for, if not all, most of the "messy punctuations". Only after replacing them with their original form, we use the "Ascii filter" to drop the rows containing invalid characters (e.g., the full stop from the Chinese input method), which our model cannot process.
