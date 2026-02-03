-- Databricks notebook source
-- MAGIC %md
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img
-- MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
-- MAGIC     alt="Databricks Learning"
-- MAGIC   >
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # 2.3 Lab - Import Data into Databricks
-- MAGIC ### Duration: ~15 minutes
-- MAGIC
-- MAGIC In this lab, you will ingest a series of JSON files and create a table (Delta table) from a Databricks volume.
-- MAGIC
-- MAGIC ### Objectives
-- MAGIC - Demonstrate how to create a table by ingesting multiple raw JSON files stored in a Databricks volume using either `COPY INTO` or the `read_files` function.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## REQUIRED - SELECT A SHARED SQL WAREHOUSE
-- MAGIC
-- MAGIC Before executing cells in this notebook, please select the **SHARED SQL WAREHOUSE** in the lab. Follow these steps:
-- MAGIC
-- MAGIC 1. Navigate to the top-right of this notebook and click the drop-down to select compute (it might say **Connect**). Complete one of the following below:
-- MAGIC
-- MAGIC    a. Under **Recent resources**, check to see if you have a **shared_warehouse SQL**. If you do, select it.
-- MAGIC
-- MAGIC    b. If you do not have a **shared_warehouse** under **Recent resources**, complete the following:
-- MAGIC
-- MAGIC     - In the same drop-down, select **More**.
-- MAGIC
-- MAGIC     - Then select the **SQL Warehouse** button.
-- MAGIC
-- MAGIC     - In the drop-down, make sure **shared_warehouse** is selected.
-- MAGIC
-- MAGIC     - Then, at the bottom of the pop-up, select **Start and attach**.
-- MAGIC
-- MAGIC <br></br>
-- MAGIC    <img src="../Includes/images/sql_warehouse.png" alt="SQL Warehouse" width="600">

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## A. Classroom Setup
-- MAGIC
-- MAGIC Run the following cell to configure your working environment for this notebook.
-- MAGIC
-- MAGIC **NOTE:** The `DA` object is only used in Databricks Academy courses and is not available outside of these courses. It will dynamically reference the information needed to run the course in the lab environment.
-- MAGIC
-- MAGIC ### IMPORTANT LAB INFORMATION
-- MAGIC
-- MAGIC Recall that your lab setup is created with the [0 - REQUIRED - Course Setup and Data Discovery]($../0 - REQUIRED - Course Setup and Data Discovery) notebook. If you end your lab session or if your session times out, your environment will be reset, and you will need to rerun the Course Setup notebook.

-- COMMAND ----------

-- MAGIC %run ../Includes/2.3-Classroom-Setup

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Lab Scenario
-- MAGIC
-- MAGIC You are an analyst at DB Inc., and you’ve been tasked with an assignment to ingest JSON files into a table. The company has placed several JSON files in the volume **dbacademy_retail.v01.retail-pipeline.customers.stream_json**, and your job is to read these JSON files into a structured table for later analysis.
-- MAGIC
-- MAGIC Follow the steps below.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Start by viewing your default catalog and schema. Confirm that your current catalog is **samples** and your current schema is **nyctaxi**.

-- COMMAND ----------

<FILL-IN>

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC SELECT current_catalog(), current_schema()

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Modify the default catalog and schema to the following:
-- MAGIC
-- MAGIC     - Set **dbacademy** as the default catalog.
-- MAGIC
-- MAGIC     - Set your **labuser** schema as the default schema. When setting the default schema, use the `IDENTIFIER` clause with the `DA.schema_name` variable to set your schema.
-- MAGIC
-- MAGIC     Run the cell and confirm that your default catalog and schema have been modified.
-- MAGIC

-- COMMAND ----------

<FILL-IN>


---- Run below to confirm the default catalog and schema were modified
SELECT current_catalog(), current_schema()

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC USE CATALOG dbacademy;
-- MAGIC USE SCHEMA IDENTIFIER(DA.schema_name);
-- MAGIC
-- MAGIC ---- Run below to confirm the default catalog and schema were modified
-- MAGIC SELECT current_catalog(), current_schema()

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Display all of the JSON files in the **/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/** volume programmatically. Confirm that your volume contains 31 JSON files.
-- MAGIC
-- MAGIC **HINTS:**
-- MAGIC   - First, navigate to the volume using the navigation bar on the right to manually view the files.
-- MAGIC   - Then, use the [LIST Statement](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-aux-list) to programmatically list all of the JSON files in the volume. You can insert the path of the volume using the UI.

-- COMMAND ----------

<FILL-IN>

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC LIST '/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/'

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Query the JSON files to view the raw JSON data. This is a good way to see exactly how the JSON files are structured. Notice that each JSON files contains a list of dictionaries, where each dictionary represents a row of data.
-- MAGIC
-- MAGIC **HINTS:**
-- MAGIC   - [Query the data by path](https://docs.databricks.com/aws/en/query#query-data-by-path) to view the raw JSON files using `text` keyword.  
-- MAGIC   - The path to volume is `/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/`. Make sure to surround the volume path in backticks.
-- MAGIC   - Add a `LIMIT` option to limit the results to 10 rows.
-- MAGIC   - You can also download one of the JSON files from the volume and open it in your favorite editor as another approach to view the raw files.
-- MAGIC
-- MAGIC
-- MAGIC **Small Example of the JSON File:**
-- MAGIC ```JSON
-- MAGIC [
-- MAGIC     {
-- MAGIC         "name": "Brent Chavez",
-- MAGIC         "email": "nelsonjoy@example.com",
-- MAGIC         "address": "568 David Brook Apt. 524",
-- MAGIC         "city": "Norwalk",
-- MAGIC         "state": "CA",
-- MAGIC         "zip_code": "45049",
-- MAGIC         "operation": "NEW",
-- MAGIC         "timestamp": 1632417981,
-- MAGIC         "customer_id": 23056
-- MAGIC     },
-- MAGIC     {
-- MAGIC         "name": "James Cruz",
-- MAGIC         "email": "perkinsdeborah@example.net",
-- MAGIC         "address": "741 Wendy Plains Apt. 143",
-- MAGIC         "city": "San Francisco",
-- MAGIC         "state": "CA",
-- MAGIC         "zip_code": "42872",
-- MAGIC         "operation": "NEW",
-- MAGIC         "timestamp": 1632421305,
-- MAGIC         "customer_id": 23057
-- MAGIC     },
-- MAGIC     ...
-- MAGIC ]
-- MAGIC ```

-- COMMAND ----------

<FILL-IN>

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC SELECT *
-- MAGIC FROM text.`/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/`
-- MAGIC LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. For a tabular display of the JSON files, query the files using `SELECT * FROM json.`. This will help you explore what the JSON files will look like as a table using the default arguments. Depending on the JSON file structure, this will read in as a table differently.
-- MAGIC
-- MAGIC     **HINTS:**
-- MAGIC       - [Query the data by path](https://docs.databricks.com/aws/en/query#query-data-by-path) to view the raw JSON files using `json`.
-- MAGIC       - Add a `LIMIT` option to limit the results to 10 rows.

-- COMMAND ----------

<FILL-IN>

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC SELECT *
-- MAGIC FROM json.`/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/`
-- MAGIC LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 6. Now that you have explored the JSON files, your goal is to:
-- MAGIC     - Create a table named **customers_lab** in the **dbacademy.labuser** schema.
-- MAGIC
-- MAGIC     - Use the JSON files in **/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/**.
-- MAGIC
-- MAGIC     - You can use either the `COPY INTO` statement or the `read_files` function.
-- MAGIC
-- MAGIC <br></br>
-- MAGIC **HINTS:**
-- MAGIC - [COPY INTO](https://docs.databricks.com/aws/en/sql/language-manual/delta-copy-into)
-- MAGIC   - With `COPY INTO`, you will need to create a table first.
-- MAGIC     - You can create the schema for the table.
-- MAGIC     - If you create the table without a schema, look at the `COPY_OPTIONS ('mergeSchema' = 'true')` option to merge the schema when adding to the table.
-- MAGIC
-- MAGIC - [read_files table-valued function](https://docs.databricks.com/aws/en/sql/language-manual/functions/read_files)
-- MAGIC

-- COMMAND ----------

<FILL-IN>

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC
-- MAGIC
-- MAGIC -- read_files solution
-- MAGIC DROP TABLE IF EXISTS customers_lab;
-- MAGIC
-- MAGIC CREATE OR REPLACE TABLE customers_lab AS
-- MAGIC SELECT *
-- MAGIC FROM read_files(
-- MAGIC   '/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/',
-- MAGIC   format => 'json'
-- MAGIC );
-- MAGIC
-- MAGIC
-- MAGIC -- COPY INTO solution
-- MAGIC DROP TABLE IF EXISTS customers_lab;
-- MAGIC
-- MAGIC CREATE TABLE customers_lab;
-- MAGIC
-- MAGIC COPY INTO customers_lab
-- MAGIC FROM '/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/'
-- MAGIC FILEFORMAT = JSON
-- MAGIC COPY_OPTIONS ('mergeSchema' = 'true');

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 7. Run the following query to view your table. Confirm the following:
-- MAGIC     - The **customers_lab** table contains 1,467 rows
-- MAGIC
-- MAGIC     - The table contains the columns: **address, city, customer_id, email, name, operation, state, timestamp, zip_code**

-- COMMAND ----------

SELECT *
FROM customers_lab;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
