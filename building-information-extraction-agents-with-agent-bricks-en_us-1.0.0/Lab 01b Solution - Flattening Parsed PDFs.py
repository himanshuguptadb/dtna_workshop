# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img
# MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
# MAGIC     alt="Databricks Learning"
# MAGIC   >
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Lab - Flattening Parsed PDFs
# MAGIC _Tech Summit 2025_
# MAGIC
# MAGIC This notebook will be attached to the already existing Job called **parse_pdfs_to_delta** to the task also called **parse_pdfs_to_delta**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Environment Setup
# MAGIC
# MAGIC This notebook relies on Environment version 2. We need to ensure that the **Environment version** is set to 2.
# MAGIC 1. Navigate to the environment icon to the right of your workspace and click on it. 
# MAGIC 1. Under **Environment version** click on the dropdown menu and select 2. 
# MAGIC 1. Click **Apply**. 
# MAGIC 1. On the pop-up screen that says **Confirm action**, click **Confirm**. 
# MAGIC > See [here](https://docs.databricks.com/aws/en/compute/serverless/dependencies) for more information on configuring a serverless environment.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC Run the following cell to configure your working environment for this notebook. This will take about 1 minute to complete.
# MAGIC
# MAGIC **NOTE:** The `DA` object is only used in Databricks Academy courses and is not available outside of these courses. It will dynamically reference the information needed to run the course in your lab environment.

# COMMAND ----------

# MAGIC %run ./Includes/Lab-Setup-01b

# COMMAND ----------

# MAGIC %md
# MAGIC Navigate to **Catalog** and locate the table created as a part of Step 1 from Lab-Setup-01a `01_single_pdf_parsed`. Use the UI to inspect the data and schema. You will find that it has a column `raw_parsed VARIANT`. You will need to flatten this column and save the results as `02_pdf_parsed_flattened`. 
# MAGIC
# MAGIC #### Instructions:
# MAGIC - Inspect the Delta table `01_single_pdf_parsed` to help understand the data. 
# MAGIC - Create a table called `02_pdf_parsed_flattened` from `01_single_pdf_parsed` that does the following:
# MAGIC 1. Rename `path` as `source_doc`. 
# MAGIC 1. Cast `page_id` as an INT and rename it as `page_number`.
# MAGIC 1. Cast `id` as INT and rename it as `element_id`.
# MAGIC 1. Cast `type` as STRING and rename it as `element_type`. 
# MAGIC 1. Cast `content` as STRING and keep the same name, `content`. 
# MAGIC 1. Leverage `variant_explode()`. 
# MAGIC
# MAGIC ##### Review of TVF `variant_explode()`
# MAGIC This table-valued function takes in a VARIANT expression, representing a VARIANT object or VARIANT ARRAY and outputs three columns
# MAGIC - `pos INT`
# MAGIC - `key STRING`
# MAGIC - `value VARIANT`
# MAGIC
# MAGIC When exploding a VARIANT object, the output key and value columns represent the keys and values of the object. When exploding a VARIANT array, the output key is always NULL, and the output value column represents the elements of the array.
# MAGIC > For more information, see [this documentation](https://docs.databricks.com/gcp/en/sql/language-manual/functions/variant_explode).

# COMMAND ----------

# MAGIC %md
# MAGIC You might find it useful to use the `DA` object for building your SQL query. **Do not change the following cell. We will revisit it in a moment to parameterize our notebook**.

# COMMAND ----------

catalog_name = DA.catalog_name
schema_name = DA.schema_name
target_table_name = '02_pdf_parsed_flattened'
source_table_name = '01_single_pdf_parsed'
# target_table_name = dbutils.widgets.get('target_table_name')
# source_table_name = dbutils.widgets.get('source_table_name')

# COMMAND ----------

df = spark.read.table('01_single_pdf_parsed')
display(df)

spark.sql(f"""
    CREATE OR REPLACE TABLE {catalog_name}.{schema_name}.{target_table_name} AS (
        SELECT
            path AS source_doc,
            CAST(value:page_id AS INT) AS page_number,
            CAST(value:id AS INT) AS element_id,
            CAST(value:type AS STRING) AS element_type,
            CAST(value:content AS STRING) AS content
        FROM {source_table_name},
        LATERAL variant_explode(raw_parsed:document:elements)
    )
""")

# COMMAND ----------

# MAGIC %md
# MAGIC If the previous table ran correctly, then you will have created a table in your catalog called `02_pdf_parsed_flattened`.

# COMMAND ----------

# MAGIC %md
# MAGIC Finally, we will need to parameterize this notebook since we will be integrating it with our Job. Let's create two widgets that bring in `02_pdf_parsed_flattend` and 
# MAGIC `01_single_pdf_parsed`. In the cell that defines variables for our tables, uncomment the `dbutils.widgets.get()` commands and comment-out the hard-coded names of the tables. 
# MAGIC </br>
# MAGIC </br>
# MAGIC
# MAGIC ```
# MAGIC catalog_name = DA.catalog_name
# MAGIC schema_name = DA.schema_name
# MAGIC # target_table_name = '02_pdf_parsed_flattend'
# MAGIC # source_table_name = '01_single_pdf_parsed'
# MAGIC target_table_name = dbutils.widgets.get('target_table_name')
# MAGIC source_table_name = dbutils.widgets.get('source_table_name')
# MAGIC ```
# MAGIC Be sure to update your code above to account for rerunning this notebook. _Hint: we want to overwrite our table each time we run this notebook at this stage in development to make sure our target table reflects our expectations with each write_.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC Congrats! Assuming you filled out the todo items correctly, this notebook is now ready to integrate into the Job `parse_pdfs_to_delta`. Navigate back to **Lab 01a - Building Information Extraction Agents with Agent Bricks** to continue the Lab.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
