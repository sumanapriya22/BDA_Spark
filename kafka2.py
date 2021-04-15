
from pyspark.sql.session import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import explode, split, col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from textblob import TextBlob
from pyspark.sql.functions import udf, col, lower, regexp_replace
import re
from pyspark.ml.feature import Tokenizer, StopWordsRemover
from nltk.stem.snowball import SnowballStemmer
from pyspark.sql.functions import when



def preprocessing(lines):
    words = lines.select(col("text").alias("word"))
    words = words.na.replace('', None)
    words = words.na.drop()
    words = words.withColumn('word', regexp_replace('word', r'http\S+', ''))
    words = words.withColumn('word', regexp_replace('word', '@\w+', ''))
    words = words.withColumn('word', regexp_replace('word', '#', ''))
    words = words.withColumn('word', regexp_replace('word', 'RT', ''))
    words = words.withColumn('word', regexp_replace('word', ':', ''))
    return words

def polarity_detection(text):
    return TextBlob(text).sentiment.polarity
def subjectivity_detection(text):
    return TextBlob(text).sentiment.subjectivity
def text_classification(words):
    # polarity detection
    polarity_detection_udf = udf(polarity_detection, StringType())
    words = words.withColumn("polarity1", polarity_detection_udf("word"))
    
    words2 = words.withColumn("polarity", when((words["polarity1"] > 0.1) & (words["polarity1"] < 0.5),"Positive")
                                 .when((words["polarity1"] >= 0.5),"Very positive")
                                 .when((words["polarity1"] < -0.1) & (words["polarity1"] > -0.5) ,"Negative")
                                 .when((words["polarity1"] <= -0.5),"Very negative")
                                 .otherwise("Neutral"))
    # subjectivity detection
    #subjectivity_detection_udf = udf(subjectivity_detection, StringType())
    #words = words.withColumn("subjectivity", subjectivity_detection_udf("word"))
    return words2.drop("polarity1")

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("wordCounter").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    # Read the data from kafka
    schem = StructType([StructField("text", StringType(), True)])
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "BDA_Spark") \
        .option("startingOffsets", "earliest") \
        .load() \
        .withColumn("value", col("value").cast("string")) \
        .select(from_json(col("value"), schem).alias("opc"))

    df.printSchema()
    #df1 = df.selectExpr("CAST(value AS STRING)")
    
    
    
    
    
    
    ds = df.select("opc.text")
    ds.printSchema()
    # df1 = ds.select((lower(regexp_replace('text', "[^a-zA-Z\\s]", "")).alias('text')))
    
    df1 = ds.na.drop()
    
    df2 = preprocessing(df1)
    
    df3 = text_classification(df2.na.drop())
    
    # tokenizer = Tokenizer(inputCol='text', outputCol='words_token')
    # df_words_token = tokenizer.transform(df1).select('words_token')

    query = df3\
        .writeStream\
        .option("checkpointLocation", "checkpoint") \
        .format("csv") \
        .option("path", "CSV") \
        .start()
        
    query.awaitTermination()