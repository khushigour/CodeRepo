# Databricks notebook source
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SparkDataframesSummary.com").getOrCreate()

# COMMAND ----------

#create Empty RDD
rdd1= spark.sparkContext.emptyRDD()
rdd2 = spark.sparkContext.parallelize([])
print(rdd1)
print(rdd2)

#Create dataframe from empty rdd and print it
# df1 = rdd1.toDF()
# df1.printSchema()

#will givr value error as rdd is empty and you are trying operations on it without providing schema

# COMMAND ----------

#Empty Dataframe from schema
#First we create RDD then convert to dataframe
from pyspark.sql.types import StructField, StructType, StringType, IntegerType
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

df1 = rdd1.toDF(schema)
df1.printSchema()
df2 = spark.createDataFrame([], schema)
df2.printSchema()

# COMMAND ----------

#create rdd with some data
employee = [("Tom", 25, "Data Engineer"), ("Tris", 32, "Software Engineer"), ("Pranay", 26, "Data Analyst")]
rdd3 = spark.sparkContext.parallelize(employee)

#create dataframe
df3 = rdd3.toDF()
df3.printSchema()

#show the dataframe created
df3.show(truncate=False)

#by default columns are named as  _1, _2, _3...
columnNames = ["name", "age", "department"]
df4 = rdd3.toDF(columnNames)
df4.show(truncate=False)

#create dataframe using "createDataFrame"
df4 = spark.createDataFrame(rdd3, schema = columnNames)
df4.show(truncate=False)
#use schema made using StructType
columnNewNames = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("department", StringType(), True)
])
df5 = spark.createDataFrame(rdd3, schema = columnNewNames)
df5.show(truncate=False)

# COMMAND ----------

#convert pyspark dataframe to pandas dataframe
pandasDF = df5.toPandas()

#Options in show : def show(self, n=20, truncate=True, vertical=False):
#2: number of rows , by default = 20 rows
#truncate: truncate content to 10 characters
df5.show(2, truncate = 10, vertical=True)

# COMMAND ----------

from pyspark.sql.types import ArrayType

#nested StructType schema
nestedSchema = StructType([
    StructField("Department", StructType([
            StructField("name", StringType(), True),
            StructField("id", IntegerType(), True)
    ]), True),
    StructField("employeeFirstName", StringType(), True),
    StructField("employeeLastName", StringType(), True),
    StructField("techstack", ArrayType(StringType()), True),
    StructField("salary", IntegerType(), False)
])

nestedData = [(("Software Engineer", 1), "Ananya", "Singh", ["Java", "python"], 4000), 
              (("Data Engineer", 2), "william", "Smith", ["Spark", "python", "hive"], 6000)]
df6 = spark.createDataFrame(data=nestedData,  schema=nestedSchema)
df6.printSchema()
df6.show(truncate=False)

# COMMAND ----------

#add or change from existing struct
#you can add multiple if (when) conditions
from pyspark.sql.functions import col,struct,when
changedDf = df6.withColumn("NewCategory", 
                           struct(col("employeeFirstName").alias("name"),
                                  col("salary").alias("salary"),
                                  when(col("salary").cast(IntegerType())<=4000, "MEDIUM")   
                                  .otherwise("HIGH").alias("Salary_Category")
                                  )).drop("employeeFirstName", "salary", "employeeLastName", "techstack")

changedDf.show()

#get schema in json format
print(changedDf.schema.json())

# COMMAND ----------

#make schema from json
import json
schemaFromJson = StructType.fromJson(json.loads('schema.json'))
df8 = spark.createDataFrame(
        spark.sparkContext.parallelize(),schemaFromJson)
df8.printSchema()

# COMMAND ----------

from pyspark.sql import Row
data=[Row(name="James",prop=Row(hair="black",eye="blue")),
      Row(name="Ann",prop=Row(hair="grey",eye="black"))]
df7=spark.createDataFrame(data)
df7.printSchema()

df7.select(df7.prop.hair).show()
df7.select(col("prop.*")).show()

# COMMAND ----------


