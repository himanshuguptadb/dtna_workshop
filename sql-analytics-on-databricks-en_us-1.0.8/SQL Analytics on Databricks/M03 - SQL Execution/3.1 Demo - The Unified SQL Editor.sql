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
-- MAGIC # 3.1 Demo - The Unified SQL Editor
-- MAGIC
-- MAGIC In this demonstration, we will compare writing SQL queries in a notebook versus using the Databricks SQL Editor.
-- MAGIC
-- MAGIC
-- MAGIC ### Objectives
-- MAGIC - Understand how to use Focus Mode for SQL within a notebook.
-- MAGIC - Explore the features and capabilities of the Unified SQL Editor.

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

-- MAGIC %run ../Includes/3.1-Classroom-Setup

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Run the following cell to view your default catalog and schema. Confirm that your default catalog is **dbacademy**, and your schema is your **labuser** schema.

-- COMMAND ----------

SELECT current_catalog(), current_schema()

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Use the Notebook Cell in SQL Focus Mode
-- MAGIC Cell focus mode expands the cell and works for Python, SQL, markdown and more. 
-- MAGIC
-- MAGIC - **Open focus mode** icon: ![open_focus_mode.png](../Includes/images/focus_mode.png) 
-- MAGIC <br></br>
-- MAGIC - **Exit focus mode** icon: ![open_focus_mode.png](../Includes/images/focus_mode_exit.png)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. In the cell below hover your mouse over the cell and select the **Open focus mode** icon ![open_focus_mode.png](../Includes/images/focus_mode.png). This opens the cell in focus mode and provides some additional features.

-- COMMAND ----------

-- Exploring Focus Mode

-- 1. Quickly explore Focus Mode by selecting the focus mode icon.

-- 2. Run the queries by selecting the "Run Cell" (play) icon above.

-- 3. View multiple results in the output and create visualizations as needed.

-- 4. Exit Focus Mode by selecting the icon at the top-right of the cell.

SELECT *
FROM aus_customers;


SELECT *
FROM aus_opportunities;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## C. Unified SQL Editor
-- MAGIC Throughout this course, we've been using an SQL notebook to execute DBSQL. Using the notebook allows us to incorporate markdown text during training.
-- MAGIC
-- MAGIC However, as a developer, you might prefer to use a native SQL editor, especially if you have experience with one in another SQL development environment. In Databricks, you can use the Unified SQL Editor for a more developer focused experience with specific features.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C1. Copy the Unified SQL Editor Instructions

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. In the left navigation right click on the file **3.1b - Unified SQL Editor Directions.txt** and select **Open in new tab**. Then copy the contents of the file to your clipboard.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C2. Opening and Using the Unified SQL Editor
-- MAGIC
-- MAGIC 1. In the far left main navigation pane right click on **SQL Editor** and select **Open in New Tab**. This will take you directly to the editor.
-- MAGIC
-- MAGIC 2. Click the **SQL Query** tab under the *Create New* section, or click the **plus icon (`+`)** next to *New tab* and select **New Query** to start a fresh SQL editor session.
-- MAGIC
-- MAGIC 3. Paste the directions from step **C1** that you copied into the query editor. Then follow those instructions.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
