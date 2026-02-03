# Databricks notebook source
from pyspark.sql.functions import regexp_replace, regexp_extract
from pyspark.sql.types import StructType, StructField, StringType

df = spark.sql("SELECT current_user() AS current_user")
current_user = df.first()["current_user"]
df = df.withColumn("schema_name", regexp_replace(regexp_extract("current_user", r"([^@]+)", 1), r"\.", "_"))
schema_name = df.first()["schema_name"]

catalog = 'dbacademy'

schema = StructType([
    StructField("owner", StringType(), True),
    StructField("object", StringType(), True),
    StructField("key", StringType(), True),
    StructField("value", StringType(), True)
])

meta = spark.createDataFrame([], schema)
#display(meta)

from pyspark.sql import Row
data = []
data = [
    Row(owner=f"{current_user}", object=None, key="username", value=f"{current_user}"),
    Row(owner=f"{current_user}", object=None, key="catalog_name", value="dbacademy"),
    Row(owner=f"{current_user}", object=None, key="schema_name", value=f"{schema_name}"),
    Row(owner=f"{current_user}", object=None, key="paths.working_dir", value=f"/Volumes/dbacademy/{schema_name}/{schema_name}"),
    Row(owner=f"{current_user}", object=None, key="warehouse_name", value=f"shared_warehouse"),
    Row(owner="account users", object=None, key="datasets.databricks_simulated_canada_sales_and_opportunities_data", value="databricks_simulated_canada_sales_and_opportunities_data.v01"),
    Row(owner="account users", object=None, key="datasets.databricks_simulated_australia_sales_and_opportunities_data", value="databricks_simulated_australia_sales_and_opportunities_data.v01"),
    Row(owner=f"{current_user}", object=None, key="pseudonym", value=f"{schema_name}")
]

new_meta = spark.createDataFrame(data, meta.schema)
meta = meta.unionByName(new_meta)
#display(meta)
spark.sql(f'USE CATALOG {catalog}')
spark.sql(f'USE SCHEMA {schema_name}')
meta.createOrReplaceTempView("meta")

# COMMAND ----------

# MAGIC %sql
# MAGIC --USE CATALOG dbacademy;  -- Modify to use DBACADEMY in Vocareum
# MAGIC --USE SCHEMA ops;
# MAGIC
# MAGIC -- Creates View of keys + values
# MAGIC CREATE OR REPLACE TEMP VIEW user_info AS
# MAGIC SELECT map_from_arrays(collect_list(key), collect_list(value)) AS config_map
# MAGIC FROM meta;
# MAGIC
# MAGIC -- Creates MAP object of ops table key + values using the view
# MAGIC DECLARE OR REPLACE DA MAP<STRING,STRING>;
# MAGIC SET VAR DA = (SELECT config_map FROM user_info);
# MAGIC
# MAGIC -- Set default schema for the user  
# MAGIC USE SCHEMA IDENTIFIER(DA.schema_name);
# MAGIC
# MAGIC SELECT current_catalog() as CourseCatalog, current_schema() as YourSchema;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE au_opportunities AS 
# MAGIC   SELECT * FROM databricks_simulated_australia_sales_and_opportunities_data.v01.opportunities;
# MAGIC CREATE OR REPLACE TABLE au_orders AS 
# MAGIC   SELECT * FROM databricks_simulated_australia_sales_and_opportunities_data.v01.orders;
# MAGIC CREATE OR REPLACE TABLE au_customers AS 
# MAGIC   SELECT * FROM databricks_simulated_australia_sales_and_opportunities_data.v01.customers;
# MAGIC
# MAGIC DROP TABLE IF EXISTS au_products;
# MAGIC
# MAGIC CREATE TABLE au_products (productid string, productname string, listprice float);
# MAGIC
# MAGIC INSERT INTO
# MAGIC   au_products (productid, productname, listprice)
# MAGIC VALUES
# MAGIC   ('JQ9322', 'TableSaw', 24.99),
# MAGIC   ('A802a', 'Mill', 10.17),
# MAGIC   ('EE05x', 'Press', 363.02),
# MAGIC   ('R9S10', 'Lathe', 43.83),
# MAGIC   ('BC111d', 'Drill', 63.28),
# MAGIC   ('W8931', 'Planer', 45.22),
# MAGIC   ('Q28R3', 'Grinder', 176.33),
# MAGIC   ('MDb304', 'CAD System', 502.80),
# MAGIC   ('OR307p', 'Kazoo', 0.99); 
# MAGIC
# MAGIC -- Show the user their catalog + schema, since they will need to interpolate their schema into lab instructions
# MAGIC SELECT current_catalog() as CourseCatalog, current_schema() as YourSchema;
