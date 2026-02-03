# Databricks notebook source
# MAGIC %pip install -qqq -U databricks-sdk databricks-langchain databricks-vectorsearch langsmith>=0.1.125 langchain==0.3.27 mlflow-skinny[databricks]>=3.4.0 
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ./new_dataset

# COMMAND ----------

DA = DBAcademyHelper()
DA.init()

# COMMAND ----------

DA.validate_table(f"{DA.catalog_name}.{DA.schema_name}.e_commerce_product_listings_dataset")

# Read dataset from marketplace
dataset = spark.sql(f"""
    SELECT 
        ASIN AS id,
        CONCAT(
            '## Title: ', Title, '\n\n',
            '## Description: ', Description, '\n\n',
            '## URL: ', URL
        ) AS document
    FROM {DA.catalog_name}.{DA.schema_name}.e_commerce_product_listings_dataset
""")

# Create a delta table for the dataset
vs_source_table_name = f"{DA.catalog_name}.{DA.schema_name}.product_text"
dataset.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(vs_source_table_name)

# Enable Change Data Feed for Delta table
spark.sql(f"ALTER TABLE {vs_source_table_name} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
