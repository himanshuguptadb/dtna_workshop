-- Databricks notebook source
-- DBTITLE 1,Cell 1
-- MAGIC %python
-- MAGIC from pyspark.sql.functions import regexp_replace, regexp_extract
-- MAGIC
-- MAGIC df = spark.sql("SELECT current_user() AS current_user")
-- MAGIC current_user = df.first()["current_user"]
-- MAGIC df = df.withColumn("schema_name", regexp_replace(regexp_extract("current_user", r"([^@]+)", 1), r"\.", "_"))
-- MAGIC schema_name = df.first()["schema_name"]

-- COMMAND ----------

-- MAGIC %py
-- MAGIC from pyspark.sql.types import StructType, StructField, StringType
-- MAGIC
-- MAGIC schema = StructType([
-- MAGIC     StructField("owner", StringType(), True),
-- MAGIC     StructField("object", StringType(), True),
-- MAGIC     StructField("key", StringType(), True),
-- MAGIC     StructField("value", StringType(), True)
-- MAGIC ])
-- MAGIC
-- MAGIC meta = spark.createDataFrame([], schema)
-- MAGIC #display(meta)

-- COMMAND ----------

-- MAGIC %py
-- MAGIC from pyspark.sql import Row
-- MAGIC data = []
-- MAGIC data = [
-- MAGIC     Row(owner=f"{current_user}", object=None, key="username", value=f"{current_user}"),
-- MAGIC     Row(owner=f"{current_user}", object=None, key="catalog_name", value="dbacademy"),
-- MAGIC     Row(owner=f"{current_user}", object=None, key="schema_name", value=f"{schema_name}"),
-- MAGIC     Row(owner=f"{current_user}", object=None, key="paths.working_dir", value=f"/Volumes/dbacademy/{schema_name}/{schema_name}"),
-- MAGIC     Row(owner=f"{current_user}", object=None, key="cluster_name", value=f"{schema_name}"),
-- MAGIC     Row(owner="account users", object=None, key="datasets.wine_quality", value="databricks_wine_quality_data.v01"),
-- MAGIC     Row(owner="account users", object=None, key="paths.datasets.wine_quality", value="/Volumes/databricks_wine_quality_data/v01"),
-- MAGIC     Row(owner="account users", object=None, key="datasets.airbnb", value="dbacademy_airbnb.v01"),
-- MAGIC     Row(owner="account users", object=None, key="paths.datasets.airbnb", value="/Volumes/databricks_airbnb/v01"),
-- MAGIC     Row(owner=f"{current_user}", object=None, key="pseudonym", value=f"{schema_name}")
-- MAGIC ]
-- MAGIC
-- MAGIC new_meta = spark.createDataFrame(data, meta.schema)
-- MAGIC meta = meta.unionByName(new_meta)
-- MAGIC meta.createOrReplaceTempView("meta")
-- MAGIC #display(meta)

-- COMMAND ----------

-- CREATE DA VARIABLE USING SQL FOR USER INFORMATION FROM THE META TABLE

-- Create a temp view storing information from the obs table.
CREATE OR REPLACE TEMP VIEW user_info AS
SELECT map_from_arrays(collect_list(replace(key,'.','_')), collect_list(value))
FROM meta;

-- Create SQL dictionary var (map)
DECLARE OR REPLACE DA MAP<STRING,STRING>;

-- Set the temp view in the DA variable
SET VAR DA = (SELECT * FROM user_info);

DROP VIEW IF EXISTS user_info;

-- COMMAND ----------

-- Set the default catalog + schema
USE CATALOG dbacademy;
USE SCHEMA IDENTIFIER(DA.schema_name);

-- COMMAND ----------

-- Check to make sure all necessary tables are in the user's schema. Otherwise return an error message
DECLARE OR REPLACE VARIABLE user_table_count INT DEFAULT 7;

DECLARE OR REPLACE VARIABLE required_table_list ARRAY<STRING> 
  DEFAULT ARRAY('aus_customers', 'aus_opportunities', 'aus_orders',  
                'ca_customers', 'ca_opportunities', 'ca_orders','au_products_lookup');

