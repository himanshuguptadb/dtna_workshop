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
# MAGIC # 0 - REQUIRED - Course Setup and Data Discovery
# MAGIC
# MAGIC This notebook is designed to set up the lab environment for this course and must be run before you proceed any further in the demonstrations and labs. The next few cells of this notebook will create the necessary data for the course.
# MAGIC
# MAGIC After the lab environment is set up, you will immediately proceed to the first demonstration lesson, "Data Discovery in Unity Catalog." This lesson will guide you through the Databricks UI to explore the environment and the data for this course.
# MAGIC
# MAGIC ### Objectives
# MAGIC - Locate catalogs, schemas, tables, and views within the Catalog Explorer.
# MAGIC - Review the permissions, settings, and metadata available in Catalog Explorer.

# COMMAND ----------

# MAGIC %md
# MAGIC ## REQUIRED - SELECT SERVERLESS COMPUTE
# MAGIC
# MAGIC Before executing cells in this notebook, please select **Serverless** compute in the upper right where it says **Connect**. The course setup script requires Python to set up the course environment.
# MAGIC
# MAGIC Follow these steps to select **Serverless**:
# MAGIC
# MAGIC 1. Navigate to the top-right of this notebook and click the drop-down menu to select compute (the drop-down should say **Connect**).
# MAGIC
# MAGIC 2. Select **Serverless**.
# MAGIC
# MAGIC **NOTE:** This is the only notebook that requires **Serverless** compute, as we need Python to set up the environment. The remaining notebooks will use an SQL **shared_warehouse**.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC Run the following cell to configure your working environment for this notebook. Confirm that the note *COURSE SETUP COMPLETE!* appears when the program completes.
# MAGIC
# MAGIC **NOTES:** 
# MAGIC - The `DA` object is only used in Databricks Academy courses and is not available outside of these courses. It will dynamically reference the information needed to run the course in the lab environment.
# MAGIC - REQUIRED - Please make sure you have selected **Serverless** compute for this cell.

# COMMAND ----------

# MAGIC %run ./Includes/0-Classroom-Setup-REQUIRED

# COMMAND ----------

# MAGIC %md
# MAGIC # 1.1 Demo - Data Discovery in Unity Catalog
# MAGIC ## A. Explore the Course Folders and Files

# COMMAND ----------

# MAGIC %md
# MAGIC 1. Complete the following steps to explore the available course folders and files:
# MAGIC
# MAGIC    a. In the left navigation bar directly to the left select the folder icon ![Folder Icon](./Includes/images/folder_icon.png). Here you will see a variety of folders for the course:
# MAGIC     - **M01 - Data Discovery**
# MAGIC
# MAGIC     - **M02 - Data Importing**
# MAGIC
# MAGIC     - **M03 - SQL Execution**
# MAGIC
# MAGIC     - **M04 - Query Analysis**
# MAGIC
# MAGIC     - **0 - REQUIRED - Course Setup and Data Discovery** notebook
# MAGIC
# MAGIC     - Each folder corresponds to a course section and contains the necessary notebooks for the demonstrations and labs.
# MAGIC
# MAGIC    b. Select the **MO1 - Data Discovery** folder. Notice this folder contains a notebook.
# MAGIC
# MAGIC    c. Use the <-- arrow to navigate back to the main course folder **SQL Analytics on Databricks**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Explore the Available Catalogs, Schemas and Data Objects

# COMMAND ----------

# MAGIC %md
# MAGIC ### B1. Explore Data Objects Using the Navigation Pane
# MAGIC 1. Complete the following to explore the available Catalogs and Data Objects using the left navigation pane:
# MAGIC
# MAGIC    a. In the left navigation pane, select the Catalog icon ![Catalog Icon](./Includes/images/catalog_icon.png). Notice there are a variety of Catalog groups:
# MAGIC
# MAGIC     - **My organization** - Available Catalogs that you can access and/or view.
# MAGIC
# MAGIC     - **Delta Shares Received** - Delta sharing catalogs (read only).
# MAGIC
# MAGIC     - **Legacy** - The legacy **hive_metastore**. We will not use this in the course. Databricks recommends using Unity Catalog for registering and governing all database objects, but also provides legacy support for Hive metastore for managing schemas, tables, views, and functions.
# MAGIC
# MAGIC    b. Expand the **dbacademy** catalog. Here you will see available **schemas (or databases)**.
# MAGIC
# MAGIC     - You will have a unique schema named something like: **labuser1234_5678**. You will be using this schema throughout the course.
# MAGIC
# MAGIC     - The **information_schema** is a SQL standard-based schema, provided in every catalog created on Unity Catalog. Within the information schema, you can find a set of views describing the objects known to the schema’s catalog that you are privileged to see. You'll learn more about these throughout this course.
# MAGIC
# MAGIC    c. Expand your **labuser** schema. You should have two data objects:
# MAGIC
# MAGIC     - **Tables** - Tables are a collection of data organized by rows and columns. The **Tables** object will also include **views**.
# MAGIC
# MAGIC     - **Volumes** - Volumes are Unity Catalog objects representing a logical volume of storage in a cloud object storage location. Volumes provide capabilities for accessing, storing, governing, and organizing non-tabular data files.
# MAGIC
# MAGIC    d. Expand **Tables**. Notice that you have access to a variety of tables in this lab.
# MAGIC
# MAGIC    e. Expand **Volumes**. Notice that you have one volume called **myfiles** in this lab. Remember, volumes store non-tabular files like `.txt`, `.parquet`, `.csv`, and more.

# COMMAND ----------

# MAGIC %md
# MAGIC ### B2. Explore a Catalog Using the Catalog Explorer
# MAGIC 2. Next, let's use the Catalog Explorer interface to view our data objects. Complete the following steps to open the Catalog Explorer and view information about the Catalog:
# MAGIC
# MAGIC    a. In the left navigation pane, select the **dbacademy** Catalog.
# MAGIC
# MAGIC    b. To the right, select the three ellipses (or kebab menu icon) and choose **Open in Catalog Explorer**. This will open the Catalog Explorer for the **dbacademy** Catalog in a new tab of your browser.
# MAGIC
# MAGIC    c. Here, we can see information about the **dbacademy** Catalog. Notice that we can see three available schemas in the Catalog, similar to the schemas we saw in the left navigation pane.
# MAGIC
# MAGIC    d. In the Catalog Explorer, select the **Details** tab. Here, you can see specific details about the catalog.
# MAGIC
# MAGIC    e. Select the **Permissions** tab. Here, you can see available permissions for the catalog. In this lab, all account users have the ability to use this catalog and see only the specific objects that apply to them.
# MAGIC
# MAGIC    f. Leave the Catalog Explorer open.

# COMMAND ----------

# MAGIC %md
# MAGIC ### B3. Explore a Schema Using the Catalog Explorer
# MAGIC 3. Complete the following to use the Catalog Explorer to view information about your schema:
# MAGIC
# MAGIC    a. Navigate back to the **Overview** tab in the Catalog Explorer.
# MAGIC
# MAGIC    b. Select your schema **labuser**. Now you can view data objects in your lab schema.
# MAGIC
# MAGIC    c. First, you can see all of the available tables in your schema. Using the buttons, you can view **Tables**, **Volumes**, **Models**, and **Functions** if you have those data objects.
# MAGIC
# MAGIC    d. Select the **Details** tab. Notice you can see information about your schema.
# MAGIC
# MAGIC    e. Select the **Permissions** tab. Here you can see the permissions associated with this schema. In your schema, your lab user account has *ALL PRIVILEGES* available on the schema.
# MAGIC
# MAGIC    f. Leave the Catalog Explorer open.

# COMMAND ----------

# MAGIC %md
# MAGIC ### B4. Explore a Table Using the Catalog Explorer
# MAGIC 4. Complete the following to use the Catalog Explorer to view information about a table in your schema:
# MAGIC
# MAGIC    a. In the Catalog Explorer, select the **Overview** tab. You should see a list of tables in your lab schema.
# MAGIC
# MAGIC    b. Select the **aus_opportunities** table. Here, you can see information about the table.
# MAGIC
# MAGIC    c. In the **Overview** tab, you can see an overview of your table. Notice the following:
# MAGIC
# MAGIC     - The Databricks Data Intelligence Platform provides AI suggestions that you can use to provide a summary of your table and columns.
# MAGIC
# MAGIC     - You can see a list of all columns in your table.
# MAGIC
# MAGIC     - On the right-hand side below **About this table**, you can see detailed information about the table, such as the  **Owner**, **Type**, **Data source**, **Popularity**, **Last updated** and **Size**.
# MAGIC
# MAGIC     - Below the **About this table** section, you can add **Tags** and a **Row filter** to the table.
# MAGIC
# MAGIC    d. Let's add the **AI Suggested Description** to the table by selecting **Accept**.
# MAGIC
# MAGIC    e. Let's add AI-generated comments to columns by selecting **AI Generate**. A list of **Comments** should appear. Simply select the checkmark for the first column, **opportunityid**.
# MAGIC
# MAGIC    f. Select the **Sample Data** tab to view a sample of the data.
# MAGIC
# MAGIC    g. Select the **Details** tab to view detailed information about the table. Notice the following:
# MAGIC
# MAGIC     - This table is a *MANAGED* table.
# MAGIC
# MAGIC     - You can see the cloud storage location of the table.
# MAGIC
# MAGIC     - You can see specific Delta table properties of the table.
# MAGIC
# MAGIC     - You can see who created the table.
# MAGIC
# MAGIC    h. Select the **Permissions** tab to view table permissions. In this example, you created the table, so you have *ALL PRIVILEGES* on this table.
# MAGIC
# MAGIC    i. Select **Grant**. Here, you can grant others specific permissions to use this table. Select **Cancel**.
# MAGIC
# MAGIC    j. Select the **History** tab. Here, you can see the history of changes to this table. In this example, you should see three versions:
# MAGIC
# MAGIC     - The initial table creation.
# MAGIC
# MAGIC     - The modification of the summary that we completed with AI.
# MAGIC
# MAGIC     - The column comments we added with AI.
# MAGIC
# MAGIC    k. Select the **Lineage** tab to view the lineage of the table. Notice that the **dbacademy_aus_sales.v01.opportunities** is shown. This is because the setup script used this table to create a table in our schema.
# MAGIC
# MAGIC    l. Select **See lineage graph** on the far right. This will display a visual representation of the lineage of the table. Again, our table was created using the **dbacademy_aus_sales.v01.opportunities** table. Close the graph.
# MAGIC
# MAGIC    m. Select the **Insights** tab to view the most frequent recent queries and users of any table registered in Unity Catalog. The Insights tab reports on frequent queries and user access for the past 30 days. In this example, the table is new, and there are no insights.
# MAGIC
# MAGIC    n. Select the **Quality** tab to create a monitor to track changes in data quality and statistical distribution. In this demonstration, we will not create a monitor, but the option is there.
# MAGIC
# MAGIC    o. Close the Catalog Explorer.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Explore Databricks Marketplace

# COMMAND ----------

# MAGIC %md
# MAGIC 1. Complete the following to explore Databricks Marketplace:
# MAGIC
# MAGIC    a. In the far left pane, right-click on **Marketplace** and select *Open in a New Tab*.
# MAGIC
# MAGIC    b. Select the filter icon to the left of the search bar ![Filter Marketplace Icon](./Includes/images/marketplace_filter_icon.png).
# MAGIC
# MAGIC    c. Under **Providers**, find *Databricks*.
# MAGIC
# MAGIC    d. Here are the data objects that Databricks shares through the Marketplace.
# MAGIC
# MAGIC    e. Scroll to the bottom of the page and select **Show more** until the option disappears.
# MAGIC
# MAGIC    f. Search for the *Simulated Australia Sales and Opportunities Data* share and select it.
# MAGIC
# MAGIC    g. This is one of the shares that is used in this course.
# MAGIC
# MAGIC    h. At the top right of the share, select **Get Instant Access**. This will open this Marketplace share, which we have already set up in this lab within Catalog Explorer. Our catalog name for the share is **dbacademy_aus_sales**. 
# MAGIC
# MAGIC    **NOTE:** If you did not have this catalog shared, you could access it by selecting **Request access** where **Open** was located.
# MAGIC
# MAGIC    i. Leave Catalog Explorer open.

# COMMAND ----------

# MAGIC %md
# MAGIC 2. Let's explore the Marketplace Share catalog that is set up in our lab in Catalog Explorer.
# MAGIC
# MAGIC    a. In the Catalog Explorer that you opened in the previous step, you might be on a table within the Marketplace catalog. At the top, select the catalog name **dbacademy_aus_sales**.
# MAGIC
# MAGIC    b. In the left navigation bar within the Catalog Explorer, you can see under the section **Delta Shares Received** that we are exploring the shared catalog from Databricks Marketplace, which has been set up for you, named **dbacademy_aus_sales**.
# MAGIC
# MAGIC    c. In the Catalog Explorer, on the right-hand side under **About this catalog**, you can see that the **Type** is *Delta Sharing*.
# MAGIC
# MAGIC    d. Select the **Permissions** tab. Notice that you have a variety of permissions on this catalog; however, you cannot write to this catalog because it is a shared catalog.
# MAGIC
# MAGIC    e. Close the Catalog Explorer.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
