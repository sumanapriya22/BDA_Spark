## Prerequisites

* Kafka(Confluent or apache)
* Pyspark (docker notebook or local installation)
* ELK stack
* Filebeat

## Architecture

![Architecture](https://user-images.githubusercontent.com/82575873/114900828-da6b8e00-9e31-11eb-946e-7d7e683bb7f3.png)

## Implementation

* Step - 1(Python code that reads tweets and sends to Kafka)
 
 * After getting access to Twitter Developer api, we stored the required keys (consumer_key,consumer_secret,access_token,access_secret) in the twitter config file
 * We have filtered the tweets based on keyword (Sample : COVID-19) and sent the tweet to the kafka topic that was created using kafka commandline
 * We have printed the tweets on the console and also verified that tweets are being sent using a kafka consumer

![KafkaConsumer](https://user-images.githubusercontent.com/82575873/114902237-3e428680-9e33-11eb-8abd-75ce059ae291.JPG)

* Step - 2 (Pyspark to analyze and apply sentiment analysis)

** 
