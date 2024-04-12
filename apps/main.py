from pyspark.sql import SparkSession
from pyspark.sql.functions import col,date_format

def init_spark():
  sql = SparkSession.builder\
    .appName("trip-app")\
    .config("spark.jars", "/opt/spark-apps/postgresql-42.2.22.jar")\
    .getOrCreate()
  sc = sql.sparkContext
  return sql,sc

def main():
  url = "jdbc:postgresql://demo-database:5432/postgres"
  properties = {
    "user": "postgres",
    "password": "casa1234",
    "driver": "org.postgresql.Driver"
  }
  file = "/opt/spark-data/MTA_2014_08_01.csv"
  sql,sc = init_spark()

  df = sql.read.load(file,format = "csv", inferSchema="true", sep="\t", header="true")
  
  # Filter invalid coordinates
  df.write \
    .jdbc(url=url, table="mta_reports", mode='append', properties=properties) \
    .save()
  
if __name__ == '__main__':
    main()
