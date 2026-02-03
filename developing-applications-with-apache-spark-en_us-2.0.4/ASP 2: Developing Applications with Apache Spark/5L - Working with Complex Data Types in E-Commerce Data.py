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
# MAGIC # 5L - Working with Complex Data Types in E-Commerce Data
# MAGIC
# MAGIC In this lab, you'll practice working with complex data types in Spark, including handling JSON strings, converting them to structured types, and manipulating nested data structures.
# MAGIC
# MAGIC ## Scenario
# MAGIC
# MAGIC You are a data engineer at an e-commerce company that collects data about customer orders, product reviews, and customer browsing behavior. The data contains nested structures that need to be properly processed for analysis.
# MAGIC
# MAGIC ### Objectives
# MAGIC - Convert JSON string data to Spark SQL native complex types
# MAGIC - Work with arrays and structs
# MAGIC - Use functions like explode, collect_list, and pivot
# MAGIC - Extract and analyze valuable insights from nested data

# COMMAND ----------

# MAGIC %md
# MAGIC ## REQUIRED - SELECT CLASSIC COMPUTE
# MAGIC
# MAGIC Before executing cells in this notebook, please select your classic compute cluster in the lab. Be aware that **Serverless** is enabled by default.
# MAGIC
# MAGIC Follow these steps to select the classic compute cluster:
# MAGIC
# MAGIC 1. Navigate to the top-right of this notebook and click the drop-down menu to select your cluster. By default, the notebook will use **Serverless**.
# MAGIC
# MAGIC 1. If your cluster is available, select it and continue to the next cell. If the cluster is not shown:
# MAGIC
# MAGIC     - In the drop-down, select **More**.
# MAGIC
# MAGIC     - In the **Attach to an existing compute resource** pop-up, select the first drop-down. You will see a unique cluster name in that drop-down. Please select that cluster.
# MAGIC
# MAGIC **NOTE:** If your cluster has terminated, you might need to restart it in order to select it. To do this:
# MAGIC
# MAGIC 1. Right-click on **Compute** in the left navigation pane and select *Open in new tab*.
# MAGIC
# MAGIC 1. Find the triangle icon to the right of your compute cluster name and click it.
# MAGIC
# MAGIC 1. Wait a few minutes for the cluster to start.
# MAGIC
# MAGIC 1. Once the cluster is running, complete the steps above to select your cluster.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Classroom Setup
# MAGIC
# MAGIC Run the following cell to configure your working environment for this course. It will set your default catalog to **dbacademy** and the schema to your specific schema name shown below using the `USE` statements.
# MAGIC
# MAGIC Also, It will create a temp table for you named `ecommerce_raw`
# MAGIC <br></br>
# MAGIC
# MAGIC ```
# MAGIC USE CATALOG dbacademy;
# MAGIC USE SCHEMA dbacademy.<your unique schema name>;
# MAGIC ```
# MAGIC
# MAGIC **NOTE:** The `DA` object is only used in Databricks Academy courses and is not available outside of these courses. It will dynamically reference the information needed to run the course.

# COMMAND ----------

# MAGIC %run ./Includes/Classroom-Setup-5L

# COMMAND ----------

# MAGIC %md
# MAGIC #### Querying the newly created table

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ecommerce_raw

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Load and Inspect Raw Data with JSON Strings
# MAGIC The raw data contains nested JSON strings (arrays and/or objects). Load and examine the retail dataset that includes these JSON strings.

# COMMAND ----------

## Read the sample dataset
events_df = spark.read.table("ecommerce_raw")

## Examine the schema and display sample data
<FILL-IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Read the sample dataset
# MAGIC events_df = spark.read.table("ecommerce_raw")
# MAGIC
# MAGIC ## Examine the schema and display sample data
# MAGIC events_df.printSchema()
# MAGIC display(events_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Convert JSON Strings to Structured Types
# MAGIC
# MAGIC The `tags` and `browsing_history` columns are arrays of String elements, and `recent_orders` is a column containing objects. Let's convert them to proper Spark structured types.

# COMMAND ----------

# 1. Get a sample of the JSON strings in each column
# 2. Infer schemas from the JSON samples
# 3. Convert the JSON strings to structured types using from_json and display the resulting DataFrame

# COMMAND ----------

## Get a sample of the JSON strings
<FILL-IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Get sample JSON strings
# MAGIC tags_json = events_df.select("tags").limit(1).collect()[0][0]
# MAGIC recent_orders_json = events_df.select("recent_orders").limit(1).collect()[0][0]
# MAGIC browsing_history_json = events_df.select("browsing_history").limit(1).collect()[0][0]
# MAGIC
# MAGIC print("Tags sample:", tags_json)
# MAGIC print("\nRecent orders sample:", recent_orders_json)
# MAGIC print("\nBrowsing history sample:", browsing_history_json)

# COMMAND ----------

## Infer schemas from the JSON samples
<FILL-IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Infer schemas from the JSON samples
# MAGIC
# MAGIC ## Define/infer schemas
# MAGIC tags_schema = schema_of_json(lit(tags_json))
# MAGIC recent_orders_schema = schema_of_json(lit(recent_orders_json))
# MAGIC browsing_history_schema = schema_of_json(lit(browsing_history_json))

# COMMAND ----------

## Convert the JSON strings to structured types using from_json and display the resulting DataFrame
parsed_df = <FILL-IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC parsed_df = events_df.select(
# MAGIC     "customer_id",
# MAGIC     "name",
# MAGIC     "email",
# MAGIC     "registration_date",
# MAGIC     from_json("tags", tags_schema).alias("tags"),
# MAGIC     from_json("recent_orders", recent_orders_schema).alias("recent_orders"),
# MAGIC     from_json("browsing_history", browsing_history_schema).alias("browsing_history")
# MAGIC )
# MAGIC
# MAGIC ## Examine the schema and display sample data
# MAGIC parsed_df.printSchema()
# MAGIC display(parsed_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Working with Arrays
# MAGIC
# MAGIC Now that we have proper structured data, let's analyze the customer tags and browsing history.

# COMMAND ----------

# 1. Calculate the number of tags and browsing history items for each customer
# 2. Explode the tags array to see all unique customer tags
# 3. Find the most common browsing categories across all customers
# HINT: use the `array_size` function or its alias `size`

# COMMAND ----------

## Calculate the number of tags and browsing history items for each customer
array_sizes_df = <FILL-IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Calculate the number of tags and browsing history items for each customer
# MAGIC array_sizes_df = parsed_df.select(
# MAGIC     "customer_id",
# MAGIC     "name",
# MAGIC     size("tags").alias("num_tags"),
# MAGIC     size("browsing_history").alias("num_browsing_categories")
# MAGIC )
# MAGIC
# MAGIC display(array_sizes_df)

# COMMAND ----------

## Explode tags to analyze customer categorization
exploded_tags_df = <FILL-IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Explode tags to see all customer categorizations
# MAGIC exploded_tags_df = parsed_df.select(
# MAGIC     "customer_id",
# MAGIC     "name",
# MAGIC     explode("tags").alias("tag")
# MAGIC )
# MAGIC
# MAGIC display(exploded_tags_df)

# COMMAND ----------

## Find the most common customer tags
tag_counts_df = <FILL-IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Find the most common customer tags
# MAGIC ## Count frequency of each tag
# MAGIC tag_counts_df = exploded_tags_df.groupBy("tag").count().orderBy(desc("count"))
# MAGIC display(tag_counts_df)

# COMMAND ----------

# 1. Explode the recent_orders array to analyze individual orders
# 2. Calculate total revenue per customer

# COMMAND ----------

## Explode the recent_orders array to analyze individual orders
orders_df = <FILL-IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Explode recent_orders to analyze individual orders
# MAGIC orders_df = parsed_df.select(
# MAGIC     "customer_id",
# MAGIC     "name",
# MAGIC     explode("recent_orders").alias("order")
# MAGIC )
# MAGIC
# MAGIC ## Calculate total revenue per customer
# MAGIC customer_revenue_df = orders_df.groupBy(
# MAGIC     "customer_id",
# MAGIC     "name"
# MAGIC ).agg(
# MAGIC     sum("order.total").alias("total_revenue"),
# MAGIC     count("order.order_id").alias("order_count")
# MAGIC ).orderBy(desc("total_revenue"))
# MAGIC
# MAGIC display(customer_revenue_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Bonus Challenge: Analyze Customer Purchasing Patterns
# MAGIC
# MAGIC Let's use the `collect_list` and `collect_set` aggregate functions to create summaries of customer purchasing patterns.

# COMMAND ----------

## First, create a flattened view of orders
order_items_df = orders_df.select(
    "customer_id",
    "name",
    "order.order_id",
    "order.date",
    explode("order.items").alias("item")
)

## Now extract the name field from each item
item_details_df = order_items_df.selectExpr(
    "customer_id",
    "name",
    "item.name as product_name"
)

# Inspect the data
display(item_details_df)

# COMMAND ----------

## Collect all products purchased by each customer, creating new columns called "all_products_purchased" and "unique_products_purchased" for each "customer_id"
customer_products_df = <FILL-IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Collect all products purchased by each customer, creating new columns called "all_products_purchased" and "unique_products_purchased" for each "customer_id"
# MAGIC customer_products_df = item_details_df.groupBy(
# MAGIC     "customer_id"
# MAGIC ).agg(
# MAGIC     collect_list("product_name").alias("all_products_purchased"),
# MAGIC     collect_set("product_name").alias("unique_products_purchased")
# MAGIC )
# MAGIC
# MAGIC display(customer_products_df)

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
