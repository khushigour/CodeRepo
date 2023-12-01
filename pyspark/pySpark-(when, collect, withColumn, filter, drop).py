# Databricks notebook source
#create Column class object
from pyspark.sql.functions import lit
colObj = lit("columnName")

employee = [("Tom", 25, "Data Engineer", ["Java", "Spark", "Hive"]), 
            ("Tris", 32, "Software Engineer", ["Java", "Springboot", "SQL"]),
             ("Pranay", 26, "Data Analyst", ["python", "pandas", "matplotlib"])]
#create dataframe
df = spark.createDataFrame(employee).toDF("name", "age", "About.person", "techstack")
df.printSchema()
df.show(truncate=False)

df.select(df.name).show()
df.select("age").show()
#backticks if '.' in column name
df.select(df["`About.person`"]).show()

from pyspark.sql.functions import col
df.select(col("`About.person`"), col("name")).show()

# COMMAND ----------

data=[(100,2,1),(200,3,4),(300,4,4)]
df2=spark.createDataFrame(data).toDF("col1","col2","col3")

#Arthmetic operations
df2.select(df2.col1 + df2.col2).show()
df2.select(df2.col1 - df2.col2).show() 

from pyspark.sql.functions import when
#when and otherwise
df2.select(df2.col1, df2.col2, df2.col3, 
           when(df2.col2 <3 , "Small")
          .when(df2.col2 <4, "Medium")
          .otherwise("High").alias("Grade")).show()

df2.select(df2.colRegex("`^.*col.*`")).show();

# COMMAND ----------

#collect 
collectData = df2.collect()

for row in collectData:
    print(row["col1"])

# COMMAND ----------

# withColumn
# casting to different type
# update the value of column
# create new column from existing one
# create new column
# rename one existing column name: withColumnRenamed

df_2 = df2.withColumn("col3",col("col3").cast("Integer"))
df_2.printSchema()
df_2.show(truncate=False)

df3 = df2.withColumn("col1",col("col1")*100)
df3.printSchema()
df3.show(truncate=False) 

df4 = df2.withColumn("CopiedCol1",col("col1")* -1)
df4.printSchema()

df5 = df2.withColumn("col4", lit("USA"))
df5.printSchema()
df5.show(truncate=False) 

df6 = df2.withColumn("col5", lit("USA")).withColumn("col6",lit("Default value"))
df6.printSchema()

df2.withColumnRenamed("col2","impCol") \
  .show(truncate=False) 
  

# COMMAND ----------

#filter with multiple conditions ( '&' -> and , '|' -> or)
# startswith, endswith, contains
from pyspark.sql.functions import array_contains
namelist = ["Harry", "Hodges"]
df.filter( (df.age  == 25) & (df.name.startswith("T")) & (~df.name.isin(namelist)) ) \
    .show(truncate=False)        

df.filter(array_contains(df.techstack,"Java")) \
    .show(truncate=False)

# COMMAND ----------

# drop: drops the column mentioned
# dropDuplicates : drops the duplicates, or duplicates of the column mentioned

df6.drop("col5").show()

df7 = df6.distinct()
df7.show(truncate=False)

df6.dropDuplicates(["col5", "col6"]).show();


# COMMAND ----------


