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
-- MAGIC # 4.1 Demo - Query Insights
-- MAGIC
-- MAGIC In this demonstration, you will explore query performance, view the query history of your SQL warehouse, and learn other techniques to monitor your SQL warehouse.
-- MAGIC
-- MAGIC ### Objectives
-- MAGIC - View the performance of a query in DBSQL to identify areas for optimization.
-- MAGIC
-- MAGIC - Explore the profile of a query in DBSQL at a high level to view execution details.
-- MAGIC
-- MAGIC - Explore the query history of your SQL warehouse to track query usage and performance.
-- MAGIC
-- MAGIC - View techniques to monitor your SQL warehouse using the Databricks monitoring tool and system tables to ensure optimal performance and resource usage.

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

-- MAGIC %run ../Includes/4.1-Classroom-Setup

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. See Your Query's Performance

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. The queries below view data in the **samples.tpch.customer** and **samples.tpch.orders** tables. Run the cell below and view the results. Notice the following:
-- MAGIC
-- MAGIC    - By default, the last table, **samples.tpch.orders**, is shown in the output. This table contains order information, including the **o_custkey** column, which can be used to join with the **customers** table.
-- MAGIC
-- MAGIC    - Above the output, expand **Show 1 additional result**. This will display the **customers** table. Notice that the **customers** table contains the **c_custkey** column.

-- COMMAND ----------

SELECT *
FROM samples.tpch.customer
LIMIT 5;

SELECT *
FROM samples.tpch.orders
LIMIT 5;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. In the above cell, notice that there is a drop-down called **See performance** right below the last `LIMIT` statement. Complete the following:
-- MAGIC
-- MAGIC    a. Expand **See performance**. Notice that both queries we ran are available.
-- MAGIC
-- MAGIC    b. Select either of the queries. A pop-up will appear on the side with query information. Here, you can examine the performance of your query.
-- MAGIC
-- MAGIC    c. At the bottom of the pop-up, select **See query profile**. This will display the entire profile of the query for you to examine.
-- MAGIC
-- MAGIC    d. Close the query profile by selecting the **X** at the top right of the profile.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Let's run a more complicated query that includes an **INNER JOIN** and a **GROUP BY**, and examine the query profile at a high level. You can use the query profile to visualize the details of a query execution. The query profile helps you troubleshoot performance bottlenecks during the query’s execution.
-- MAGIC
-- MAGIC       **REQUIREMENTS:** To view a query profile, you must either be the owner of the query or you must have at least CAN MONITOR permission on the SQL warehouse that executed the query.
-- MAGIC
-- MAGIC    Complete the following:
-- MAGIC
-- MAGIC    a. Run the cell below.
-- MAGIC
-- MAGIC    b. Expand **See performance**.
-- MAGIC
-- MAGIC    c. Select the query to see the performance. Notice that this query executed in about ~2 seconds.
-- MAGIC
-- MAGIC    d. Select **See query profile**. Here, you can examine each stage of the query profile to determine how your query performed, and identify any bottlenecks or issues. We won't go into depth here, but it's good to understand the profile as you gain more experience.
-- MAGIC
-- MAGIC    ![Query Plan](../Includes/images/query_plan_join_newUI.png)

-- COMMAND ----------

SELECT 
  c.c_mktsegment,
  o.o_orderstatus,
  count(*) AS total_count
FROM samples.tpch.customer c
  INNER JOIN samples.tpch.orders o ON c.c_custkey = o.o_custkey
GROUP BY
  c.c_mktsegment,
  o.o_orderstatus
ORDER BY
  c.c_mktsegment,
  o.o_orderstatus;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Additional Resources
-- MAGIC
-- MAGIC This was a quick introduction to the query profile in Databricks. For more in-depth information, view the following resources:
-- MAGIC
-- MAGIC - [Query Profile](https://docs.databricks.com/aws/en/sql/user/queries/query-profile)
-- MAGIC
-- MAGIC - [Get to Know Your Queries with the New Databricks SQL Query Profile!](https://www.databricks.com/blog/2022/02/23/get-to-know-your-queries-with-the-new-databricks-sql-query-profile.html)
-- MAGIC
-- MAGIC - [Query caching](https://docs.databricks.com/aws/en/sql/user/queries/query-caching)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## C. View Warehouse Query History

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. You can also view the query history of your warehouse. To view the entire query history of the warehouse Complete the following:
-- MAGIC
-- MAGIC    a. On the far-left navigation pane, right-click on **Compute** and select **Open in New Tab**. This will open the available compute resources in your environment.
-- MAGIC
-- MAGIC    b. In the top navigation tabs, select **SQL Warehouses** to view your available warehouses.
-- MAGIC
-- MAGIC    c. You should see only one warehouse, **shared_warehouse** (your organization may have multiple warehouses here). Select the warehouse.
-- MAGIC
-- MAGIC    d. You will see a variety of tabs here based on your access. Your permissions in this lab environment limit what you can view.
-- MAGIC
-- MAGIC    e. At the top right of the page, you should see the three ellipses. Select them and then choose **Query history**.
-- MAGIC
-- MAGIC    f. Scroll through the page. Since this is a shared warehouse, you will see a variety of queries, many of which you did not execute.
-- MAGIC
-- MAGIC    g. Close the query history page.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Depending on your access, you may also be able to **Monitor a SQL warehouse**. In this lab, you do not have this capability, but if available, it would provide a visualization of various statistics for your warehouse, allowing you to monitor its performance.
-- MAGIC
-- MAGIC    Let's view the [Monitor a SQL warehouse](https://docs.databricks.com/aws/en/compute/sql-warehouse/monitor) documentation page for more information.
-- MAGIC
-- MAGIC
-- MAGIC ![Monitoring SQL Warehouse](../Includes/images/monitoring_sql_warehouse.png)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## D. Databricks System Tables (Public Preview as of March 2025)
-- MAGIC You can also use system tables in Databricks to monitor a variety of account information.
-- MAGIC
-- MAGIC System tables are a Databricks-hosted analytical store of your account’s operational data found in the system catalog. System tables can be used for historical observability across your account. Below are some additional links for monitoring your sql warehouse and queries with system tables. 
-- MAGIC
-- MAGIC - [Monitor account activity with system tables](https://docs.databricks.com/gcp/en/admin/system-tables/) - List of all system table
-- MAGIC
-- MAGIC   - [Query history system table reference](https://docs.databricks.com/aws/en/admin/system-tables/query-history) - Public preview as of March 2025
-- MAGIC
-- MAGIC   - [Warehouses system table reference](https://docs.databricks.com/gcp/en/admin/system-tables/warehouses) - Public preview as of March 2025 
-- MAGIC
-- MAGIC   - [Warehouse events system table reference](https://docs.databricks.com/gcp/en/admin/system-tables/warehouse-events) - Public preview as of March 2025

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
