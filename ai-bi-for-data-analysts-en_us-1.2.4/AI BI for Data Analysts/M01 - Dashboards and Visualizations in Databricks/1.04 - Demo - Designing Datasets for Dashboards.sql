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
-- MAGIC ## 1.04 Demo - Designing Datasets for Dashboards
-- MAGIC
-- MAGIC Databricks AI/BI Dashboards help you quickly transform data into shareable insights. 
-- MAGIC
-- MAGIC In this lesson, we’ll learn about creating datasets specifically for AI/BI Dashboards and how to associate a dashboard to these given assets. Datasets are the sources of information for AI/BI Dashboards. 
-- MAGIC
-- MAGIC
-- MAGIC This lesson uses the following resources:
-- MAGIC - Tables:
-- MAGIC   - Catalog: dbacademy
-- MAGIC   - Schema: {dynamically named, personal to you}
-- MAGIC   - Tables:
-- MAGIC     - ca_customers
-- MAGIC     - ca_orders
-- MAGIC     - ca_products
-- MAGIC     - ca_opportunities
-- MAGIC
-- MAGIC These tables contain simulated business-to-business order and opportunity data for an imaginary company's Canadian sales operation. The **ca_orders** table contains information from 2021 through the middle of November 2024. This table identifies the relevant customer with a unique key that points into the **ca_customers** table, and it identifies the relevant product with a unique key that points into the **ca_products** table (which you'll create). The **ca_opportunities** table provides additional details regarding sales opportunities and sales representatives. You'll use the data in these tables to prepare your dashboard.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### REQUIRED: Course Setup and Data Discovery
-- MAGIC The first thing you'll need to complete any data analytics task is the appropriate data for the request. To find the right data, you'll need to use the Catalog Explorer or the Databricks Search box to locate the data for this project. In this particular lab exercise, a setup script will copy tables from a Databricks Marketplace share into a schema you control. To get started, click the small triangle **Run** button in the top left of the cell below.

-- COMMAND ----------

-- MAGIC %run "../Includes/setup/ca_setup"

-- COMMAND ----------

-- MAGIC %md
-- MAGIC This script clones a few small data tables from a Databricks Marketplace share into your personal schema. At the end it prints out the name of your catalog and your schema. The schema will have a randomly generated name. Make a note of this value. In these instructions, we'll call this simply "your schema."
-- MAGIC
-- MAGIC To use the Databricks Catalog Explorer to see your newly loaded data, follow the steps below.
-- MAGIC
-- MAGIC 1. Select **Catalog** from the sidebar navigation.
-- MAGIC 1. In the catalog selector, locate the catalog titled: **dbacademy**. You can also use the search at the top to narrow down the available options.
-- MAGIC 1. Expand your schema. You should see three tables in this schema.
-- MAGIC     - ca_customers
-- MAGIC     - ca_orders
-- MAGIC     - ca_opportunities
-- MAGIC
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### A: Build a query in the Dashboard editor
-- MAGIC
-- MAGIC Let's build up a query we can use as our dashboard's main data source.
-- MAGIC
-- MAGIC **📌 NOTE:** Throughout these instructions, replace `YOURSCHEMA` with the name of your schema. (You can find your schema name in the setup run cell that you have just executed.) Additionally, many of the following instructions take place in a non-notebook area of the platform. It is recommended to open either the notebooks in a separate tab or window to reference the instructions alongside the area where they are performed.
-- MAGIC
-- MAGIC 1. Select **Dashboards** from the sidebar navigation. (It is recommended to right-click and select Open Link in New Window or Tab)
-- MAGIC 1. Click the **Create dashboard** button at top right.
-- MAGIC 1. In the resulting dashboard-creation screen, click the **Data** tab at the top left of the canvas. 
-- MAGIC
-- MAGIC Here, you will find three choices: **Create from SQL**, **Add data source**, and **Upload file**. 
-- MAGIC   - **Create from SQL** allows you to enter a SQL Query to select the dataset for the dashboard. 
-- MAGIC   - **Add data source** lets us search through all the available tables in Unity Catalog that you have SELECT access to. 
-- MAGIC   - **Upload file** allows you to directly upload a data file from this UI to Unity Catalog to be used with your dashboard. 
-- MAGIC
-- MAGIC 4. Choose the option, **Create from SQL**.
-- MAGIC
-- MAGIC 1. Enter this query:
-- MAGIC
-- MAGIC
-- MAGIC   ```
-- MAGIC   SELECT * FROM dbacademy.YOURSCHEMA.ca_orders ;
-- MAGIC   ```
-- MAGIC
-- MAGIC   Either replace **YOURSCHEMA** with your user specific schema or use the dropdowns to set your catalog and schema for the query. Click the **Run** button. To help us confirm this is the right data, the user interface lets us browse the results of the query at bottom. 
-- MAGIC
-- MAGIC 6. Let's focus our query only on orders from 2022. Modify the query to make it like so:
-- MAGIC
-- MAGIC ```
-- MAGIC SELECT * FROM dbacademy.YOURSCHEMA.ca_orders   
-- MAGIC  WHERE orderdate >= '2022-01-01' 
-- MAGIC        AND orderdate <= '2022-12-31' ;
-- MAGIC
-- MAGIC ```
-- MAGIC   Click the **Run** button and confirm that we are only seeing orders from 2022.
-- MAGIC
-- MAGIC
-- MAGIC 7. Let's name only the fields we need. Update and run the query once again:
-- MAGIC
-- MAGIC ```
-- MAGIC SELECT customerid, orderdate, orderamt, salesrep 
-- MAGIC   FROM dbacademy.YOURSCHEMA.ca_orders   
-- MAGIC   WHERE orderdate >= '2022-01-01' 
-- MAGIC         AND orderdate <= '2022-12-31'  ;
-- MAGIC ```
-- MAGIC
-- MAGIC
-- MAGIC 8. Now let's make the query more useful by replacing the customer ID with useful information about the customer. Update and run the query once again:
-- MAGIC
-- MAGIC ```
-- MAGIC SELECT c.customername, c.province, o.orderdate, o.orderamt, o.salesrep 
-- MAGIC  FROM dbacademy.YOURSCHEMA.ca_orders as o
-- MAGIC  JOIN dbacademy.YOURSCHEMA.ca_customers as c
-- MAGIC    ON o.customerid = c.customerid
-- MAGIC  WHERE orderdate >= '2022-01-01' AND orderdate <= '2022-12-31' ;
-- MAGIC
-- MAGIC ```
-- MAGIC
-- MAGIC
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B: Augment the Main Dataset
-- MAGIC
-- MAGIC We already replaced customer ID field with useful information: customer's name, their city, and their province (using standard Canadian province abbreviations, which are two letters). We'd like to do the same for the products, but there does not seem to be a similar table that explicates each product ID in the same way that **ca_customers** does for the customer IDs. For this we could either upload a small CSV to Databricks containing those product values (which can be found within the includes for this course) or utilize the command below. 
-- MAGIC
-- MAGIC 1. Click the Run button (small triangle) in the top-left corner of the cell below

-- COMMAND ----------

-- MAGIC %run "../Includes/setup/make_ca_products_table"
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Now return to the Databricks dashboard user interface window. Return to the Dashboards dataset definition screen. Use the **Add data source** option to select the ca_products table from your catalog or use the **Create from SQL** option to enter the query below, replacing `YOURSCHEMA` with your personal schema name:
-- MAGIC
-- MAGIC ```
-- MAGIC SELECT * from dbacademy.YOURSCHEMA.ca_products;
-- MAGIC ```
-- MAGIC Then click the **Run** button. 
-- MAGIC
-- MAGIC (If it doesn't work, confirm you replaced `YOURSCHEMA` with the name of your personal schema or set the default catalog and schema at the top of the query.)
-- MAGIC
-- MAGIC Now we have a table called **ca_products** with human-friendly information about each product. 
-- MAGIC
-- MAGIC As we don't need a query strictly for just the products table separately, delete the query from the dashboard's datasets.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C: Define the Main Dataset
-- MAGIC
-- MAGIC Returning to the query for our main dataset for our dashboard, we want to augment it with the product details. 
-- MAGIC
-- MAGIC 1. Enter the following completed query that augments the resulting data table with the product names:
-- MAGIC
-- MAGIC ```
-- MAGIC SELECT c.customername, c.province, o.orderdate, 
-- MAGIC        p.productname, o.orderamt, o.salesrep 
-- MAGIC  FROM dbacademy.YOURSCHEMA.ca_orders AS o
-- MAGIC  JOIN dbacademy.YOURSCHEMA.ca_customers AS c
-- MAGIC   ON o.customerid = c.customerid
-- MAGIC  JOIN dbacademy.YOURSCHEMA.ca_products AS p
-- MAGIC   ON o.productid = p.productid
-- MAGIC  WHERE orderdate >= '2022-01-01' 
-- MAGIC        AND orderdate <= '2022-12-31' ;
-- MAGIC
-- MAGIC ```
-- MAGIC
-- MAGIC 2. Click **Run** to confirm it works.
-- MAGIC 1. Click on the kebab menu in the “Untitled dataset” box, choose Rename, and name the query **Orders22**.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D: Add a Dataset for the 2024 Sales Goal
-- MAGIC
-- MAGIC 1. Still in the **Data** tab, select the **+ Create from SQL** option.
-- MAGIC 2. Enter the following query into the query editing space:
-- MAGIC ```
-- MAGIC   SELECT 
-- MAGIC       sum(orderamt) AS Total_Sales, 390000000 AS Sales_Goal 
-- MAGIC   FROM 
-- MAGIC       dbacademy.YOURSCHEMA.ca_orders
-- MAGIC   WHERE 
-- MAGIC       orderdate >= '2024-01-01' AND orderdate <= '2024-12-31' ;
-- MAGIC
-- MAGIC ```
-- MAGIC 3. Click **Run** to execute the query. 
-- MAGIC 4. Right-click the newly created query in the **Datasets** list and select **Rename**, or use the kebab menu, to rename the dataset it constitutes as **SumTotalSales**.
-- MAGIC
-- MAGIC Now your dashboard has a total of two datasets.
-- MAGIC
-- MAGIC **NOTE:** If you want to use automatic formatting for your dataset queries, you can right click in the query screen and select **Format document**.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### E: Name the Dashboard
-- MAGIC
-- MAGIC Your dashboard gets a placeholder name when you create it. You should always rename your dashboard to something that reminds you and others of its intended purpose. 
-- MAGIC
-- MAGIC 1. At the top left of the dashboard definition panel, you'll see the placeholder dashboard name, which will be something like `New Dashboard 202X-01-01 12:00:00`. Click on it and change its name to **Canada Sales**.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
