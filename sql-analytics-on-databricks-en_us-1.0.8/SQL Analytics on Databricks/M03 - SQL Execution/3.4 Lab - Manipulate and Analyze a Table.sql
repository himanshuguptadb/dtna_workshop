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
-- MAGIC # 3.4 Lab - Manipulate and Analyze a Table
-- MAGIC
-- MAGIC ### Duration: ~15-20 minutes
-- MAGIC
-- MAGIC In this lab, you will manipulate a **bronze layer** table to create a **silver layer** table. Then, you will create a scheduled **materialized view** to perform some simple analysis on the table and refresh it daily.
-- MAGIC
-- MAGIC
-- MAGIC ### Objectives
-- MAGIC - Apply basic data transformation techniques to clean and structure raw data for further analysis
-- MAGIC - Combine data from multiple sources and perform necessary operations to derive meaningful insights
-- MAGIC - Create and manage views that aggregate data and automate refresh processes for improved and more efficient analysis.

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
-- MAGIC Recall that your lab setup is created with the [0 - REQUIRED - Course Setup]($../0 - REQUIRED - Course Setup and Data Discovery) notebook. If you end your lab session or if your session times out, your environment will be reset, and you will need to rerun the Course Setup notebook.

-- COMMAND ----------

-- MAGIC %run ../Includes/3.4-Classroom-Setup

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Run the following cell to set and view your default catalog and schema. Confirm that your default catalog is **dbacademy** and your schema is **labuser** (this uses the `DA.schema_name` variable created in the classroom setup script).
-- MAGIC
-- MAGIC The default catalog and schema are pre-configured for you in the cell below. This eliminates the need to specify the three-level name for your tables (i.e., catalog.schema.table). All tables will be read from and written to your **dbacademy.labuser** schema.

-- COMMAND ----------

-- Change the default catalog/schema
USE CATALOG dbacademy;
USE SCHEMA IDENTIFIER(DA.schema_name);


-- View current catalog and schema
SELECT 
  current_catalog(), 
  current_schema(), 
  DA.schema_name AS variable_value   -- Display DA.schema_name variable value

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Lab Scenario
-- MAGIC
-- MAGIC You are an analyst at DB Inc., and you’ve been assigned the task of working with customer data stored in several JSON files. The data is located in the volume **dbacademy_retail.v01.retail-pipeline.customers.stream_json**. Your goal is to clean, transform, and enrich the raw data and create two new objects:
-- MAGIC
-- MAGIC - **Silver table**: This table will contain curated, cleaned, and slightly transformed data. It serves as an intermediate stage between raw data and the gold-level table.
-- MAGIC
-- MAGIC - **Gold materialized view**: This materialized view will contain aggregated data that should be scheduled to be refreshed every day.
-- MAGIC
-- MAGIC Follow the steps detailed below.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B1. Ingestion and Exploration

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Run the following cell to create a table named **customers_lab_bronze** in your **dbacademy.labuser** schema. The data will be sourced from a series of JSON files located in the provided Marketplace shared data volume: `/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/`
-- MAGIC

-- COMMAND ----------

-- Drop the table if it already exists to start from the beginning
DROP TABLE IF EXISTS customers_lab_bronze;

-- Create an empty table
CREATE TABLE customers_lab_bronze;

-- Copy JSON files from a volume into the table, merge the schema
COPY INTO customers_lab_bronze
FROM '/Volumes/dbacademy_retail/v01/retail-pipeline/customers/stream_json/'
FILEFORMAT = JSON
COPY_OPTIONS ('mergeSchema' = 'true');

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Run the cell below to query the **customers_lab_bronze** table and preview 10 rows. Notice the following:
-- MAGIC
-- MAGIC    - The **email** column contains the user's email domain.
-- MAGIC
-- MAGIC    - The **state** column contains a U.S. state abbreviation.
-- MAGIC
-- MAGIC    - The **timestamp** column contains a Unix timestamp value.

-- COMMAND ----------

SELECT *
FROM customers_lab_bronze
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Write a query below to:
-- MAGIC
-- MAGIC    - View the distinct values in the **state** column of the **customers_lab_bronze** table and name the column **distinct_state**.
-- MAGIC
-- MAGIC    - Order the result by the new column **distinct_state** in ascending order.
-- MAGIC
-- MAGIC    Run the query and view the results. Confirm that the query returns 48 rows and that the first value is `null`.

-- COMMAND ----------

<FILL-IN>

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC SELECT distinct(state) AS distinct_state
-- MAGIC FROM customers_lab_bronze
-- MAGIC ORDER BY distinct_state;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Run the query below to query the **state_lookup** table and preview 10 rows. Notice that the table contains abbreviated state names, which can be used to obtain the full state names.

-- COMMAND ----------

SELECT *
FROM state_lookup
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B2. Data Manipulation and Transformation

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Create the **customer_lab_silver** table by completing the following:
-- MAGIC
-- MAGIC    a. Select the following columns from the **customers_lab_bronze** table:
-- MAGIC       - **customer_id**
-- MAGIC       - **name**
-- MAGIC       - **address**
-- MAGIC       - **city**
-- MAGIC       - **email**
-- MAGIC       - **operation**
-- MAGIC       - **zip_code**
-- MAGIC       - **state**
-- MAGIC
-- MAGIC    b. Create a column named **sign_up_date** by converting the Unix timestamp (**timestamp** column) to a human-readable date format using the following:
-- MAGIC       - [from_unixtime function](https://docs.databricks.com/aws/en/sql/language-manual/functions/from_unixtime)
-- MAGIC
-- MAGIC       - [date_format function](https://docs.databricks.com/aws/en/sql/language-manual/functions/date_format)
-- MAGIC
-- MAGIC       **HINT:**
-- MAGIC       ```sql
-- MAGIC       date_format(from_unixtime(timestamp), 'yyyy-MM-dd HH:mm:ss') AS sign_up_date
-- MAGIC       ```
-- MAGIC
-- MAGIC    c. Create a column named **email_domain** that extracts the domain from the email address using the `substring_index` function.
-- MAGIC       - [substring_index function](https://docs.databricks.com/aws/en/sql/language-manual/functions/substring_index#:~:text=Returns%20the%20substring%20of%20expr,occurrence%20of%20the%20delimiter%20delim%20.)
-- MAGIC
-- MAGIC       - Example results: **peter@example.org** → **example.org**
-- MAGIC
-- MAGIC       **HINT:**
-- MAGIC       ```SQL
-- MAGIC       substring_index(cust.email, '@', -1) AS email_domain,
-- MAGIC       ```
-- MAGIC
-- MAGIC    d. Perform a LEFT JOIN between the **customers_lab_bronze** and **state_lookup** tables to retain all records from the **customers_lab_bronze** table, creating the **state_name** column from the **state_lookup** table to obtain the full state name where available.
-- MAGIC       - **HINT:** Try using the `generate with AI` in another cell to assist you with the join syntax if you need it.
-- MAGIC
-- MAGIC **NOTE:** The solution table has already been created for you in your **labuser** schema if you would like to view it. The table is named **customer_lab_silver_solution**.
-- MAGIC

-- COMMAND ----------

<FILL-IN>

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC CREATE OR REPLACE TABLE customer_lab_silver AS
-- MAGIC SELECT
-- MAGIC   cust.customer_id,
-- MAGIC   cust.name,
-- MAGIC   cust.address,
-- MAGIC   cust.city,
-- MAGIC   cust.email,
-- MAGIC   cust.operation,
-- MAGIC   cust.zip_code,
-- MAGIC   cust.state,
-- MAGIC   date_format(from_unixtime(timestamp), 'yyyy-MM-dd HH:mm:ss') AS sign_up_date,
-- MAGIC   substring_index(cust.email, '@', -1) AS email_domain,
-- MAGIC   state.state_name
-- MAGIC FROM customers_lab_bronze cust
-- MAGIC   LEFT JOIN state_lookup state ON cust.state = state.state_abbreviation;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Run the cell below to compare your table **customer_lab_silver** to the solution table **customer_lab_silver_solution**. If the tables are identical (column names, all data, etc) then query should return 0 rows. 
-- MAGIC
-- MAGIC If the query returns an error, you will have to fix the **customer_lab_silver** table you created in the previous cell.

-- COMMAND ----------

SELECT *
FROM customer_lab_silver_solution
EXCEPT
SELECT
  customer_id,
  name,
  address,
  city,
  email,
  operation,
  zip_code,
  state,
  sign_up_date,
  email_domain,
  state_name
FROM customer_lab_silver;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B3. Create a Materialized View

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Run the cell below to view 10 rows from your **customer_lab_silver** table.

-- COMMAND ----------

SELECT *
FROM customer_lab_silver
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Create a materialized view named **customers_per_state_gold** that:
-- MAGIC
-- MAGIC    - Counts the number of customers by **state_name** from the **customers_lab_silver** table in a column named **total_customers**.
-- MAGIC
-- MAGIC    - Ensures the materialized view refreshes every day.
-- MAGIC
-- MAGIC    - Orders the results by **total_customers** in descending order.
-- MAGIC
-- MAGIC    [CREATE MATERIALIZED VIEW](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-materialized-view)
-- MAGIC
-- MAGIC    **HINT:** If you couldn't create the **customers_lab_silver** table correctly, you can use the premade solution table **customer_lab_silver_solution**.

-- COMMAND ----------

<FILL-IN>

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC CREATE MATERIALIZED VIEW customers_per_state_gold 
-- MAGIC SCHEDULE EVERY 1 DAY
-- MAGIC AS
-- MAGIC SELECT 
-- MAGIC   state_name, 
-- MAGIC   count(*) AS total_customers
-- MAGIC FROM customer_lab_silver 
-- MAGIC GROUP BY state_name
-- MAGIC ORDER BY total_customers DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Run the cell below to view your materialized view. Confirm your first 10 rows of your materialized view match the following values:
-- MAGIC
-- MAGIC     | state_name  | total_customers |
-- MAGIC     |-------------|-----------------|
-- MAGIC     | California  | 259             |
-- MAGIC     | Texas       | 141             |
-- MAGIC     | New York    | 98              |
-- MAGIC     | Florida     | 69              |
-- MAGIC     | Illinois    | 55              |
-- MAGIC     | Michigan    | 52              |
-- MAGIC     | Ohio        | 50              |
-- MAGIC     | null        | 49              |
-- MAGIC     | Washington  | 38              |
-- MAGIC     | Arizona     | 36              |
-- MAGIC

-- COMMAND ----------

SELECT *
FROM customers_per_state_gold;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Write the statement to describe detailed information about your materialized view **customers_per_state_gold** to view the refresh information. 
-- MAGIC
-- MAGIC    Confirm that your **# Refresh Information** section looks similar to this solution example:
-- MAGIC
-- MAGIC
-- MAGIC | **Refresh Information**     |  **Data Type**                      |
-- MAGIC |-----------------------------|-----------------------------------|
-- MAGIC | **Last Refreshed**           | 2025-03-20T20:45:05Z (will differ)             |
-- MAGIC | **Last Refresh Type**        | RECOMPUTED                        |
-- MAGIC | **Latest Refresh Status**    | Succeeded                         |
-- MAGIC | **Latest Refresh**           | Your specific refresh |
-- MAGIC | **Refresh Schedule**         | EVERY 1 DAYS                       |

-- COMMAND ----------

<FILL-IN>

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC DESCRIBE EXTENDED customers_per_state_gold;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
