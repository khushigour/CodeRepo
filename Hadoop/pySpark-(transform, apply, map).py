# Databricks notebook source
#Transform
#pyspark.sql.DataFrame.transform() - available after Spark 3.0
#pyspark.sql.functions.transform()

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Examples").getOrCreate()

columns  = ["deptId", "no_of_employees", "stack"]

data = [("cs", 23, ["dsa", "dbms", "os"]), ("me", 40, ["thermodynamics", "fluid"]), ("ee", 50, ["circuit", "currentflow"])]

df = spark.createDataFrame(data=data,schema=columns)
df.show(truncate=False)

#DataFrame.transform(func: Callable[[…], DataFrame], *args: Any, **kwargs: Any)
# func – Custom function to call.
# *args – Arguments to pass to func.
# *kwargs – Keyword arguments to pass to func.

#functions to transform data
from pyspark.sql.functions import upper
def to_upper_str_columns(df):
    return df.withColumn("deptId",upper(df.deptId))

def increase_employee(df,addedEmployees):
    return df.withColumn("no_of_employees",df.no_of_employees + addedEmployees)

df2 = df.transform(to_upper_str_columns) \
        .transform(increase_employee,10) 

df2.show(truncate=False)

#pyspark.sql.functions.transform(col, f)
# col – *ArrayType* column 
# f – Optional. Function to apply
from pyspark.sql.functions import transform
# df.select(transform("deptId", lambda x: x+"__")).alias("deptId").show()    -> error :  data type mismatch: Parameter 1 requires the "ARRAY" type
df.select(transform("stack", lambda x: upper(x))).alias("teckstack").show()

# COMMAND ----------

# apply

import pyspark.pandas as ps
import numpy as np

technologies = ({
    'Fee' :[20000,25000,30000,22000,np.NaN],
    'Discount':[1000,2500,1500,1200,3000]
               })
# Create a DataFrame
psdf = ps.DataFrame(technologies)
print(psdf)

def add(data):
   return data[0] - data[1]
   
addDF = psdf.apply(add,axis=1)
print(addDF)

# COMMAND ----------

# map
# : DataFrame doesn’t have map() transformation to use with DataFrame hence you need to DataFrame to RDD first
rdd = df.rdd.map(lambda x: ("_"+x[0]+"_", x[1]*2))  
df2=rdd.toDF(["name","employee_num"]   )
df2.show()

# COMMAND ----------

# flatMap
values = ["hello,world,big,news,today"]
rdd1 = spark.sparkContext.parallelize(values)
for element in rdd1.collect():
    print(element)
rdd2=rdd1.flatMap(lambda x: x.split(","))
for element in rdd2.collect():
    print(element)

# explode
from pyspark.sql.functions import explode
df3 = df.select(df.deptId,explode(df.stack))
df3.printSchema()
df3.show()

# COMMAND ----------


