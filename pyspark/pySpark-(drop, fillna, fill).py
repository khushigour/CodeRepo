# Databricks notebook source
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("PYSPARKexamples") \
    .getOrCreate()

data = [
    ("khushi","SDE",None),
    ("anya","SDE","A"),
    ("eren",None,None)
  ]

columns = ["name","dept","grade"]
df = spark.createDataFrame(data,columns)
df.show()

# COMMAND ----------

# drop(how='any', thresh=None, subset=None)
# how = 'all' / 'any' :  if all/any columns have null
# threshold for non-null  values, if less than that it will remove the row
# subset = define columns to check null value for
df.na.drop('all').show()
df.na.drop('any').show()

df.na.drop(subset=["dept"]) \
   .show(truncate=False)

df.dropna().show(truncate=False)


# COMMAND ----------

# Imports
from pyspark.sql.functions import col
df.filter("grade is NULL").show()
df.filter(df.grade.isNull()).show()
df.filter(col("grade").isNull()).show()


# Filtering on multiple Columns
df.filter("grade IS NULL AND dept IS NULL").show()
df.filter(df.grade.isNull() & df.dept.isNull()).show()



df.filter("grade IS NOT NULL").show()
df.filter("NOT grade IS NULL").show()
df.filter(df.grade.isNotNull()).show()
df.filter(col("grade").isNotNull()).show()

# Filtering by spark.sql
df.createOrReplaceTempView("DATA")
spark.sql("SELECT * FROM DATA where GRADE IS NULL").show()

# COMMAND ----------

df.fillna("unknown",["dept"]) \
    .fillna("",["grade"]).show()

df.fillna({"dept": "unknown", "grade": ""}) \
    .show()

df.na.fill("unknown",["dept"]) \
    .na.fill("",["grade"]).show()

# COMMAND ----------


