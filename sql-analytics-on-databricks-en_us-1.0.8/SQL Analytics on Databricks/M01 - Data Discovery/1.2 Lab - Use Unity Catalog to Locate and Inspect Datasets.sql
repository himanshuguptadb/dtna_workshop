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
-- MAGIC # 1.2 Lab - Use Unity Catalog to Locate and Inspect Datasets
-- MAGIC
-- MAGIC In this lab you will explore your environment.

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

-- MAGIC %run ../Includes/1.2-Classroom-Setup

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Use the Catalog Explorer to Answer the Questions Below
-- MAGIC
-- MAGIC Use the Catalog Explorer to answer the questions below to the best of your ability. This content isn't graded, but is designed to allow you to practice what you learned in this module and explore the Databricks Workspace UI.
-- MAGIC
-- MAGIC For detailed instructions and the answers, go to the **1.2 Lab Solution** notebook for this lab.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Explore the `samples` Catalog

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Who owns the **samples** catalog?

-- COMMAND ----------

---- Use the Catalog Explorer to find the owner.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: Databricks, Inc
-- MAGIC
-- MAGIC -- 1. Find the 'samples' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. On the right, under 'About this catalog', notice that the owner of this catalog is 'Databricks, Inc.'.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. What permissions do you have on the **samples** catalog?

-- COMMAND ----------

---- Use the Catalog Explorer to find the permissions.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: None, Permissions cannot be viewed or edited on samples data.
-- MAGIC
-- MAGIC -- 1. Find the 'samples' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. Select the 'Permissions' tab to view permissions.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. How many table(s) are in the **nyctaxi** schema (database) within the **samples** catalog?

-- COMMAND ----------

---- Use the Catalog Explorer to view the tables in the 'nyctaxi' schema.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: 1 table named 'trips'
-- MAGIC
-- MAGIC -- 1. Find the 'samples' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. Select the 'nyctaxi' schema.
-- MAGIC
-- MAGIC -- 4. You should see that the 'nyctaxi' schema contains 1 table named 'trips'.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. How many columns are in the **samples.nyctaxi.trips** table?

-- COMMAND ----------

---- Use the Catalog Explorer to view the columns in the 'trips' table.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: 6 columns are in the 'trips' table.
-- MAGIC
-- MAGIC -- 1. Find the 'samples' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. Select the 'nyctaxi' schema.
-- MAGIC
-- MAGIC -- 4. Select the 'trips' table.
-- MAGIC
-- MAGIC -- 5. View the overview of the table. Here you should see the columns in the table.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## C. Explore the `dbacademy_ca_sales` Catalog

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. What two schemas are in the **dbacademy_ca_sales** catalog?

-- COMMAND ----------

---- Use the left navigation bar to view the schemas.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: 2 schemas, 'information_schema' and 'v01'
-- MAGIC
-- MAGIC -- 1. Find the 'dbacademy_ca_sales' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Expand the catalog.
-- MAGIC
-- MAGIC -- 3. View the two schemas within the catalog.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. What type is the **dbacademy_ca_sales** catalog?

-- COMMAND ----------

---- Use the Catalog Explorer to view the 'About this catalog' section.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: Type is 'Delta Sharing' because this catalog was created using Databricks Marketplace when your lab was set up.
-- MAGIC
-- MAGIC -- 1. Find the 'dbacademy_ca_sales' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. In the 'Overview' tab, look at the far right under 'About this catalog'. Notice that the Type is 'Delta Sharing'.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. In **dbacademy_ca_sales.v01** navigate to the **customers** table. What permissions do you have on this table?

-- COMMAND ----------

---- Use the Catalog Explorer to view the permissions on the 'customers' table.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: 'SELECT'
-- MAGIC
-- MAGIC -- 1. Find the 'dbacademy_ca_sales' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. Select the 'v01' schema.
-- MAGIC
-- MAGIC -- 4. Select the 'customers' table.
-- MAGIC
-- MAGIC -- 5. Select the 'Permissions' tab.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## D. Explore your Course Schema `dbacademy.labuser_name`

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Who created the **dbacademy.labuser_name.ca_orders** table?

-- COMMAND ----------

---- Use the Catalog Explorer to view the Details of the 'ca_orders' table.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: Table was created by your 'labuser' name (example, 'labuser1234_5678').
-- MAGIC
-- MAGIC -- 1. Find the 'dbacademy' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. Select the 'labuser_name' schema.
-- MAGIC
-- MAGIC -- 4. Select the 'ca_orders' table.
-- MAGIC
-- MAGIC -- 5. Select the 'Details' tab.
-- MAGIC
-- MAGIC -- 6. Find the row 'Created By'. This table was created by your account using the setup script.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. What permissions do you have on your table **ca_orders**?

-- COMMAND ----------

---- Use the Catalog Explorer to view the permissions you have on the 'ca_orders' table.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: 'ALL PRIVILEGES'
-- MAGIC
-- MAGIC -- 1. Find the 'dbacademy' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. Select the 'labuser_name' schema.
-- MAGIC
-- MAGIC -- 4. Select the 'ca_orders' table.
-- MAGIC
-- MAGIC -- 5. Select the 'Permissions' tab.
-- MAGIC
-- MAGIC -- 6. Notice that you have 'ALL PRIVILEGES' on this table since you are the owner.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. View the history of the **ca_orders** table. What version is this table? What is the most recent **Operation**?

-- COMMAND ----------

---- Use the Catalog Explorer to view the History.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: 'Version 0', 'CREATE TABLE AS SELECT'
-- MAGIC
-- MAGIC -- 1. Find the 'dbacademy' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. Select the 'labuser_name' schema.
-- MAGIC
-- MAGIC -- 4. Select the 'ca_orders' table.
-- MAGIC
-- MAGIC -- 5. Select the 'History' tab.
-- MAGIC
-- MAGIC -- 6. Notice that this table has 1 version, 'Version 0', and this table was created using the 'CREATE TABLE AS SELECT' statement.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Add a *AI Suggested Description* to the **ca_orders** table.

-- COMMAND ----------

---- Use the Catalog Explorer to add the 'AI Suggested Description'.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: Your table should have a description.
-- MAGIC
-- MAGIC -- 1. Find the 'dbacademy' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. Select the 'labuser_name' schema.
-- MAGIC
-- MAGIC -- 4. Select the 'ca_orders' table.
-- MAGIC
-- MAGIC -- 5. Select the 'Overview' tab.
-- MAGIC
-- MAGIC -- 6. Notice that an 'AI Suggested Description' for the table is available. Select 'Accept'.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. View the history of the **ca_orders** How many versions does this table have now? What is the most recent **Operation**?

-- COMMAND ----------

---- Use the Catalog Explorer to view the History.

-- COMMAND ----------

-- MAGIC %skip
-- MAGIC -- Question Answer: '2 Versions', 'version 0', 'version 1', 'SET TBLPROPERTIES'
-- MAGIC
-- MAGIC -- 1. Find the 'dbacademy' catalog in the left navigation pane.
-- MAGIC
-- MAGIC -- 2. Select the three ellipses to the right of the catalog and select 'Open in Catalog Explorer'.
-- MAGIC
-- MAGIC -- 3. Select the 'labuser_name' schema.
-- MAGIC
-- MAGIC -- 4. Select the 'ca_orders' table.
-- MAGIC
-- MAGIC -- 5. Select the 'History' tab.
-- MAGIC
-- MAGIC -- 6. Notice that this table has '2 versions', 'Version 0' and 'Version 1'. A new version of this table has been added when you added the 'AI generated description' of this table.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
