# Databricks notebook source
employee = [("Tom", 25, "Data Engineer", ["Java", "Spark", "Hive"]), 
            ("Tris", 32, "Software Engineer", ["Java", "Springboot", "SQL"]),
            ("Ananya", 28, "Data Analyst", ["pySpark", "pandas", "numpy"]),
             ("Pranay", 26, "Data Analyst", ["python", "pandas", "matplotlib"]),
             ("Ananya", 26, "Data Engineer", ["pySpark", "Hive", "Kafka"])]

df = spark.createDataFrame(employee).toDF("name", "age", "Post", "techstack")
df.printSchema()
df.show(truncate=False)

from pyspark.sql.functions import col

df.sort("name","Post").show(truncate=False)
df.sort(df.name.asc()).show(truncate=False)
df.orderBy(col("name").asc(),col("Post").desc()).show(truncate=False)

# COMMAND ----------

#other options: sum, min, max, avg, mean
df.groupBy("Post").count().show(truncate=False)

from pyspark.sql.functions import sum,avg,max
#agg - allows to calculate various aggregations 
df.groupBy("Post") \
    .agg(avg("age").alias("avg_age"), 
      max("age").alias("max_age")).show(truncate=False) 
    # .where(col("Post") == "Data Engineer") \
   

# COMMAND ----------

# pivot 
pivotDF = df.groupBy("name").pivot("Post").sum("age")
pivotDF.printSchema()
pivotDF.show(truncate=False)

# pivot is a very expensive operation hence, it is recommended to provide column data (if known) as an argument
posts = ["Data Engineer","Software Engineer","Data Analyst"]
pivotDF = df.groupBy("name").pivot("Post", posts).sum("age")
pivotDF.show(truncate=False)

# COMMAND ----------

#JOIN
employee  = [(1, "khushi", 353, 2),
            (2, "Gojo", 432,-1),
            (3, "panda", 543, 2),
            (4, "eren", 432, 3)]

emp_schema = ["employeeId", "name", "DeptId", "managerId"]

dept = [(353, "CS"),
          (432, "AI"),
          (656, "IT")]

dept_schema = ["deptId", "deptName"]
df_employee= spark.createDataFrame(data= employee , schema= emp_schema)
df_employee.show(truncate=False)
df_dept = spark.createDataFrame(data = dept, schema = dept_schema)
df_dept.show()

#inner join
df_employee.join(df_dept, df_employee.DeptId == df_dept.deptId, "inner").show(truncate=False)

# Other options:
    # outer/full/fullouter : it shows all columns and null for those deptId is not present in other table
    # left/leftouter : shows all left columns and null for those deptId is not present in right table
    # right/rightouter : shows all right columns and null for those deptId is not present in left table
    # leftsemi: inner join but only shows columns of left table
    # leftanti: inner join but only shows columns of right table (opposite of leftsemi)
    # /self join/ : not present, but can be done using already options present

df_employee.alias("emp1").join(df_employee.alias("emp2")
                            , col("emp1.managerId")==col("emp2.employeeId"), "inner").show() \
                            .select(col("emp1.employeeId"),col("emp1.name"), 
      col("emp2.employeeId").alias("manager_emp_id"), 
      col("emp2.name").alias("manager_emp_name")) \
   .show(truncate=False)

#use sql 
df_employee.createOrReplaceTempView("EMP")
df_dept.createOrReplaceTempView("DEPT")

joinDF = spark.sql("select * from EMP e, DEPT d where e.DeptId == d.deptId") \
  .show(truncate=False)

# COMMAND ----------

#union
dept1 = [(353, "CS"),
        (432, "AI"),
        (656, "IT")]

dept2 = [(353, "CS"),
        (452, "DS"),
        (651, "DE")]

dept3 = [("CS", 353),
        ("DS", 452),
        ( "DE", 651)]

df1 = spark.createDataFrame(data = dept1, schema=["id", "name"])
df1.printSchema()

df2 = spark.createDataFrame(data = dept2, schema=["id", "name"])
df2.printSchema()

df3 = spark.createDataFrame(data = dept3, schema=["name","id"])
df3.printSchema()

#with duplicates
df_union = df1.union(df2)
df_union.show(truncate=False)

#without duplicates
unionDF = df1.union(df2).distinct()
unionDF.show(truncate=False)

# merge two DataFrames by column names
#allowMissingColumns = different number of columns, null values for missing columns
df_unionall = df1.unionByName(df3, allowMissingColumns=True)
df_unionall.printSchema()
df_unionall.show()

# COMMAND ----------


