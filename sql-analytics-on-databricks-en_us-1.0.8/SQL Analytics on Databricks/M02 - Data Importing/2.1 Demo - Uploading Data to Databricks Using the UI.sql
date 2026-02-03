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
-- MAGIC # 2.1 Demo - Uploading Data to Databricks Using the UI
-- MAGIC
-- MAGIC In this demonstration we will upload a small CSV file into a volume within Databricks using the UI. Additionally, you'll also learn how to use the Databricks file upload UI to create a Databricks managed table.
-- MAGIC
-- MAGIC ### Objectives
-- MAGIC - Demonstrate how to upload a CSV file into a volume in Databricks.
-- MAGIC - Demonstrate how to upload a CSV file to create a Databricks managed table.
-- MAGIC
-- MAGIC **NOTE:** Depending on your computer restrictions, you might not be able to complete the following demonstration, which includes downloading a CSV file locally and then using the browser to upload the file back into Databricks.

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

-- MAGIC %run ../Includes/2.1-Classroom-Setup

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Upload a Local CSV File to a Volume Using the UI
-- MAGIC
-- MAGIC In this section, we will demonstrate how to upload a local CSV file to a Databricks volume. To replicate this process, we have provided the CSV file in the **data** folder for you to download to your local computer.
-- MAGIC
-- MAGIC **Note:** Depending on your laptop’s security policies, you might not be able to download and upload a file to Databricks.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Complete the following steps to download the CSV file locally:
-- MAGIC
-- MAGIC    a. In the **M02 - Data Importing** folder, there is a **data** folder. Open the **data** folder, and you should see a file named **au_products.csv**.
-- MAGIC
-- MAGIC    b. Hover your mouse over the **au_products.csv** file, then select the three ellipses to the right of the file and choose **Download**. This will download the CSV file to your computer's download folder.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Complete the following steps to upload the CSV file to your volume:
-- MAGIC
-- MAGIC    a. In the far-left pane, right-click **Catalog** and select *Open in New Tab*.
-- MAGIC
-- MAGIC    b. In the Catalog Explorer, select the **dbacademy** catalog.
-- MAGIC
-- MAGIC    c. Select your **labuser** schema.
-- MAGIC
-- MAGIC    d. Select **Volumes**, then choose the **myfiles** volume.
-- MAGIC
-- MAGIC    e. In the upper-right corner, select **Upload to this volume**.
-- MAGIC
-- MAGIC    f. Upload the **au_products.csv** file you downloaded in the previous step.
-- MAGIC
-- MAGIC    g. Select **Upload** to upload the CSV file to the Databricks volume.
-- MAGIC
-- MAGIC    h. Close the Catalog Explorer.
-- MAGIC
-- MAGIC    **Note:** If you have the necessary permissions on your laptop to upload a file, the file will be uploaded to the **myfiles** volume.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Complete the following steps to view the CSV file in the Databricks volume:
-- MAGIC
-- MAGIC    a. In the left navigation pane, select the catalog icon ![Catalog Icon](../Includes/images/catalog_icon.png).
-- MAGIC
-- MAGIC    b. Expand the **dbacademy** catalog.
-- MAGIC
-- MAGIC    c. Expand your **labuser** schema.
-- MAGIC
-- MAGIC    d. Expand **Volumes** and your **myfiles** volume. You should see that the **au_products.csv** file has been uploaded to the Databricks volume (you might have to refresh the volume using the refresh button above the catalog search bar).
-- MAGIC
-- MAGIC    **Note:** Remember, Databricks volumes are logical storage spaces used to store and access files. They are part of Unity Catalog, which is used to govern non-tabular datasets like CSV files.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. With the CSV file in a volume, you can now programmatically display and create a table from the CSV file. We will show you how to do this in the next demonstration.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## C. Upload a Local CSV File as a Table Using the UI
-- MAGIC In this section we will upload the same **au_products.csv** file to Databricks, but this time create a table using the UI instead of uploading the CSV file directly to a volume.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Complete the following steps to upload the CSV file as a table to your schema:
-- MAGIC
-- MAGIC    a. In the far-left pane, right-click **Catalog** and select *Open in New Tab*.
-- MAGIC
-- MAGIC    b. In the Catalog Explorer, select the **dbacademy** catalog.
-- MAGIC
-- MAGIC    c. Select your **labuser** schema.
-- MAGIC
-- MAGIC    d. In the upper-right corner, select the **Create** dropdown.
-- MAGIC
-- MAGIC    e. Select **Table**.
-- MAGIC
-- MAGIC    f. Add your locally downloaded file, **au_products.csv**, to the UI.
-- MAGIC
-- MAGIC    g. Notice that the **Create or modify table from file upload** provides a variety of options to set when importing your CSV file as a table.
-- MAGIC
-- MAGIC    h. Change the name of the table to **aus_products_ui**.
-- MAGIC
-- MAGIC    i. Since this is a simple CSV file, leave the remaining options as they are and select **Create table** at the bottom right. This will create the table in Databricks from your local CSV file.
-- MAGIC
-- MAGIC    j. After the table is created, accept the **AI Suggested Description**.
-- MAGIC
-- MAGIC    **Note:** If you have the necessary permissions on your laptop to upload a file, the file will be uploaded as a new table named **aus_products_ui** to Databricks. However, your security policies might prohibit uploading a file.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. In the left navigation pane refresh your **labuser** schema. The new table **aus_products_ui** should appear in your schema.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
