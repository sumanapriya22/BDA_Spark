## Prerequisites

* Kafka(Confluent or apache)
* Pyspark (docker notebook or local installation)
* ELK stack
* Filebeat

## Architecture

![Architecture](https://user-images.githubusercontent.com/82575873/114900828-da6b8e00-9e31-11eb-946e-7d7e683bb7f3.png)

## Implementation

1.Python code that reads tweets and sends to Kafka
 
 * After getting access to Twitter Developer api, we stored the required keys (consumer_key,consumer_secret,access_token,access_secret) in the twitter config file
 * We have filtered the tweets based on keyword (Sample : COVID-19) and sent the tweet to the kafka topic that was created using kafka commandline
 * We have printed the tweets on the console and also verified that tweets are being sent using a kafka consumer

![KafkaConsumer](https://user-images.githubusercontent.com/82575873/114902237-3e428680-9e33-11eb-8abd-75ce059ae291.JPG)

2. Pyspark to analyze and apply sentiment analysis

* From kafka we have used Spark kafka connector for structured streaming and connected to our kafka topic
* We have first cleaned the data by removing spaces, non-ascii characters etc.
* We then implemented Textblob classifier for sentiment analysis
* TextBlob is a python library and offers a simple API to access its methods and perform basic NLP tasks. 
* After applying Textblod we get polarity score based on which take the Sentiment values

Polarity score  | Value
------------- | -------------
>0.1 & <0.5   |  Postive
>0.5          | Very Positive
<-0.1 & >-0.5 |  Postive
<-0.5         | Very Negative
else          |  Neutral


