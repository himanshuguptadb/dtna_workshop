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
-- MAGIC ## 2.05 Demo - Maintaining Genie Spaces
-- MAGIC
-- MAGIC Databricks AI/BI Genie empowers your end users by allowing them to have natural language chats directly with your organization's data. 
-- MAGIC
-- MAGIC In this lesson, we’ll learn how to perform the initial definition of a Genie space. 
-- MAGIC
-- MAGIC
-- MAGIC This lesson uses the following resources:
-- MAGIC - Tables:
-- MAGIC   - Catalog: dbacademy
-- MAGIC   - Schema: {dynamically named, personal to you}
-- MAGIC   - Tables:
-- MAGIC     - ca_customers
-- MAGIC     - ca_orders
-- MAGIC     - ca_opportunities
-- MAGIC     - ca_products
-- MAGIC
-- MAGIC These tables contain simulated business-to-business order and opportunity data for an imaginary company's Canadian sales operation. The **ca_orders** table contains information from 2021 through the middle of November 2024. This table identifies the relevant customer with a unique key that points into the **ca_customers** table, and it identifies the relevant product with a unique key that points into the **ca_products** table. The **ca_opportunities** table provides additional details regarding sales opportunities and sales representatives. You'll use the data in these tables to prepare your Genie space.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### REQUIRED: Course Setup and Data Discovery
-- MAGIC The first thing you'll need to complete any data analytics task is the appropriate data for the request. To find the right data, you'll need to use the Catalog Explorer or the Databricks Search box to locate the data for this project. In this particular lab exercise, a setup script will copy tables from a Databricks Marketplace share into a schema you control. To get started, click the small triangle **Run** button in the top left of the cell below.

-- COMMAND ----------

-- MAGIC %run "../Includes/setup/ca_setup_with_products_table"

-- COMMAND ----------

-- MAGIC %md
-- MAGIC This script clones a few small data tables from a Databricks Marketplace share into your personal schema. At the end it prints out the name of your catalog and your schema. The schema will have a randomly generated name. Make a note of this value. In these instructions, we'll call this simply "your schema."
-- MAGIC
-- MAGIC To use the Catalog Explorer, follow the steps below.
-- MAGIC
-- MAGIC 1. Select **Catalog** from the sidebar navigation.
-- MAGIC 1. In the catalog selector, locate the catalog titled: **dbacademy**. You can also use the search at the top to narrow down the available options.
-- MAGIC 1. Expand your schema. You should see four tables in this schema.
-- MAGIC     - ca_customers
-- MAGIC     - ca_orders
-- MAGIC     - ca_opportunities
-- MAGIC     - ca_products
-- MAGIC
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### A: Enhance Tables' Unity Catalog Metadata
-- MAGIC
-- MAGIC Genie automatically uses table and field descriptions from Unity Catalog to improve the quality of its responses. Leaving these fields blank for production tables is a missed opportunity, but it is very easy to populate them.
-- MAGIC
-- MAGIC **📌 NOTE:** Many of the following instructions take place in a non-notebook area of the platform. It is recommended to open either the notebooks in a separate tab or window to reference the instructions alongside the area where they are performed.
-- MAGIC
-- MAGIC If you're following along with this demonstration in the Vocareum lab environment, you may need to grant a Unity Catalog permission to your Vocareum username.
-- MAGIC
-- MAGIC 1. To find your Vocareum username, click on **Databricks Details** at the far top right. (You will not see this frame in a production Databricks environment.)
-- MAGIC
-- MAGIC 1. In the resulting panel, select and copy your **Email** value, an email address ending in `@vocareum.com`. This email address is your username.
-- MAGIC 1. Close the panel by clicking **Close** at top right.
-- MAGIC 1. Edit the SQL cell below, replacing YOURUSERNAME between the backquotes by pasting your copied username over it.  (Be sure not to insert a stray newline between the backquotes. The whole backquoted email address should be on one line.)
-- MAGIC 1. Click the Run triangle at top left of the SQL cell to execute it.
-- MAGIC
-- MAGIC

-- COMMAND ----------

USE CATALOG dbacademy;
USE SCHEMA ops;

CREATE OR REPLACE TEMP VIEW user_info AS
  SELECT map_from_arrays(collect_list(key), collect_list(value))
  FROM meta; 
DECLARE OR REPLACE DA MAP<STRING,STRING>;
SET VAR DA = (SELECT * FROM user_info);
USE SCHEMA IDENTIFIER(DA.schema_name);
GRANT MANAGE ON TABLE ca_orders TO `YOURUSERNAME`;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC 6. Select **Catalog** from the sidebar navigation. (It is recommended to right-click and select Open Link in New Window or Tab)
-- MAGIC 1. In the catalog selector, locate the catalog titled: **dbacademy**. You can also use the search at the top to narrow down the available options.
-- MAGIC 1. Expand your personal schema. You should see four tables in this schema.
-- MAGIC
-- MAGIC 1. Drill into the **ca_orders** table. Notice that, at top, Databricks Assistant announces that it is creating a description. In a moment, under the header **AI Suggested Description**, a textual writeup of this table's contents and usefulness appears. If it looks good to you, click **Accept**. If not, click **Edit** and correct any errors or omissions you notice, and then click **Save**.
-- MAGIC 1. Below the description, notice that no field in the table contains a description. There is a button to the left labeled **AI Generate**. Click this button. Databricks Assistant will propose descriptions for the fields.
-- MAGIC 1. Accept each suggestion. What kinds of further enhancements could you make to these fields' descriptions? Examples:
-- MAGIC - For ID fields, naming the other table into which they point
-- MAGIC - For currency fields, naming the currency (Canadian dollars, euros, etc.) in which they are expressed
-- MAGIC 12. What kinds of other enhancements could you make to the other tables' field descriptions? Consider what might be helpful for the **province** field in the **ca_customers** table. 
-- MAGIC
-- MAGIC If you had a field with a timestamp, what might be helpful to add to its description? What if you had a field that made reference to fiscal quarters?

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B: Augment Table Metadata and descriptions in a Genie space
-- MAGIC Sometimes you will not have edit permissions to the data tables you use for a Genie space. To solve for this restriction, as a Genie space administrator, you will be able to augment any table metadata from within your created Genie space. 
-- MAGIC
-- MAGIC **📌 NOTE:** Many of the following instructions take place in a non-notebook area of the platform. It is recommended to open either the notebooks in a separate tab or window to reference the instructions alongside the area where they are performed.
-- MAGIC
-- MAGIC 1. If you are not already looking at the **Canada Sales and Opportunities Current Year** Genie space, navigate to it through **Genie** in the sidebar navigation. (It is recommended to right-click and select Open Link in New Window or Tab)
-- MAGIC 1. Select **Configure** from the top left, then navigate down into **Data**. 
-- MAGIC 1. Here, you'll be presented with a list of all the data tables associated with this Genie space. Click on the **ca_orders** table. 
-- MAGIC 1. You're presented with the **Description** and a list of all the columns in the table, along with their respective column descriptions. 
-- MAGIC 1. Click the pencil icon next to **Description**. 
-- MAGIC 1. You're presented with a pop-up window to **Edit table description**. Here you can augment the table description that is being supplied from Unity Catalog. Note, edits to the description are local to the Genie space only and do not write back to Unity Catalog. 
-- MAGIC
-- MAGIC What additional information could you provide that may be relevant to the Genie space's purpose?
-- MAGIC
-- MAGIC 7. Click **Cancel** or **Save** to close the window.
-- MAGIC 1. Select a column from the list. Notice that you have the option to exclude the column from the Genie space. Select the pencil icon to edit the column description. 
-- MAGIC 1. The resulting dialog box for the column not only allows you to edit the Description for the column, but also allows you to add Synonyms for the column to improve Genie's capability to match user prompts to the column. Expand the Advanced panel.
-- MAGIC 1. In the Advanced space, you can sample Example values or build a value dictionary. Click **Cancel** or **Save** to close the pop-up.
-- MAGIC
-- MAGIC Augmenting table information with a Genie space gives you control if you do not have edit permissions on the table itself in Unity Catalog. It also allows you to enhance the Genie space's understanding of your data and it's purpose for that data. Adding table and column descriptions is always valuable, not just for Genie, but for your entire data estate.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C: Create a Benchmark
-- MAGIC
-- MAGIC Benchmarks are tools that help you proactively monitor the health of your Genie space. To create a benchmark, you can save one or more queries associated with a particular question. Benchmarks allow you to set the ground truth for a question and periodically check Genie's response to that question against your ground truth to ensure it maintain accuracy and alignment with the desired purpose. Benchmarks can be either human-scored or automatically scored. Human-scored benchmarks require a human being to inspect each of Genie's responses and confirm that it is appropriate. For automatically-scored benchmarks, Genie can compare the query's actual result to the desired result.
-- MAGIC
-- MAGIC 1. Select **Genie** from the sidebar navigation.
-- MAGIC 1. In the resulting list of Genie spaces, click on the **Canada Sales and Opportunities Current Year** Genie space.
-- MAGIC 1. Click on the **History** button from the options at the top right (the option with an icon resembling a small clock). This displays all the chats you've had with Genie.
-- MAGIC 1. Next click on the **Monitoring** button from the options at the top right (the option with an icon resembling an eye).
-- MAGIC 1. Find and select a representative query that received a thumbs-up from the human being who submitted it. This opens the question results on the right.
-- MAGIC 1. Below the response, click on **Show code**. The SQL that Genie created to answer this human query is revealed in a toggle below the response.
-- MAGIC 1. In the sidebar navigation, right-click on **Genie** and open the link in a new tab, and click on **Canada Sales and Opportunities Current Year** Genie space. 
-- MAGIC
-- MAGIC You should now have two browser tab, both open on Genie.
-- MAGIC
-- MAGIC 8. In the new browser tab, click on the **Benchmarks** button from the options at the top right (the option with an icon resembling a bar graph).
-- MAGIC 1. Click on the **+ Add benchmark** button at top right.
-- MAGIC 1. In the **Question** field of the resulting window, paste in the human query you selected from the **History** window in the other browser tab.
-- MAGIC 1. In the **Ground truth SQL answer** field of the resulting window, paste in the associated SQL from the **History** window in the other browser tab.
-- MAGIC 1. Click **Add benchmark** to save the benchmark question.
-- MAGIC 1. Now click **Run all benchmarks** to execute the query again and confirm that it still works as intended.
-- MAGIC
-- MAGIC Regularly running benchmarks is a great way to confirm that the behavior of a Genie space has not drifted in an incorrect direction as more users interact with the system and as new data arrives to its underlying tables.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
