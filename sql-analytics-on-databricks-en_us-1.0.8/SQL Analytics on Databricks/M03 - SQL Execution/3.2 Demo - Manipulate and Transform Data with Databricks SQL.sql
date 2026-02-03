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
-- MAGIC # 3.2 Demo - Manipulate and Transform Data with Databricks SQL
-- MAGIC
-- MAGIC In this demonstration we will explore, manipulate and analyze tables using DBSQL.
-- MAGIC
-- MAGIC ### Objectives
-- MAGIC - Perform simple data exploration by querying tables in DBSQL to understand the data structure, identify key columns, and examine the first few rows.
-- MAGIC - Use DBSQL functions, case statements, and joins to perform data transformation and create a new table containing modified data based on specific conditions.
-- MAGIC - Apply filtering and summary statistics in DBSQL to extract meaningful insights, using functions like WHERE, GROUP BY, and HAVING for data analysis.
-- MAGIC - Perform data analysis using common table expressions (CTEs), pivot operations, and windowing functions to extract more detailed insights and perform complex calculations

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

-- MAGIC %run ../Includes/3.2-Classroom-Setup

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
  DA.schema_name AS variable_value -- Display DA.schema_name variable value

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Data Exploration
-- MAGIC
-- MAGIC With the tables already in the **dbacademy** catalog and within the **labuser** schema, it's time to begin exploring the tables using DBSQL.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Let's start by querying the **aus_orders** table to display a preview of the table. Notice that this table contains information about customer orders in Australia.

-- COMMAND ----------

SELECT *
FROM aus_orders
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. You can view the basic metadata information of a table with the `DESCRIBE TABLE` statement. Run the query. Notice that the results show the column name, the data type, and if there is a comment on the column.
-- MAGIC
-- MAGIC     [DESCRIBE TABLE](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-aux-describe-table)

-- COMMAND ----------

DESCRIBE TABLE aus_orders;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. You can use the `DESCRIBE TABLE EXTENDED` statement to display detailed information about the specified columns, including the column statistics collected by the command and additional table metadata information.
-- MAGIC
-- MAGIC     Run the cell and view the results. Notice the following:
-- MAGIC
-- MAGIC     - From row **9**, *Detailed Table Information* is shown below.
-- MAGIC
-- MAGIC     - In the row **Created Time**, you can see when this table was created.
-- MAGIC
-- MAGIC     - In the row **Type**, you can see if the table is managed or external.
-- MAGIC
-- MAGIC     - In the row **Owner**, you can see the owner of the table.
-- MAGIC
-- MAGIC     - A variety of other detailed information about the table is shown.
-- MAGIC

-- COMMAND ----------

DESCRIBE TABLE EXTENDED aus_orders;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. View the distinct values in the **productid** column Notice that there are 7 unique **productid** values. We will later use this column to obtain the product names from the **au_products_lookup** table.

-- COMMAND ----------

SELECT DISTINCT(productid) AS distinct_productid
FROM aus_orders;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## C. Data Manipulation and Transformation
-- MAGIC
-- MAGIC After exploring the data, we will begin transforming it for downstream analysis. For training, we will break down each transformation step-by-step in each cell. For testing purposes, we will use a `LIMIT` statement to verify our logic without processing the entire dataset until necessary.
-- MAGIC
-- MAGIC In this section, we will complete the following transformations:
-- MAGIC
-- MAGIC - Rename columns by adding an underscore **_** between column names.
-- MAGIC
-- MAGIC - Standardize the values in the **salesrep** column by converting them to uppercase.
-- MAGIC
-- MAGIC - Parse the **orderdate** column into detailed components like year, month, day, quarter, etc.
-- MAGIC
-- MAGIC - Create a categorical variable based on **orderamt** to classify the order amount as *High*, *Middle*, or *Low*.
-- MAGIC
-- MAGIC - Join the **aus_orders** table with the **au_products_lookup** table to obtain the **productname**.
-- MAGIC
-- MAGIC - Create a new table named **aus_orders_silver**.
-- MAGIC
-- MAGIC For reference, here is a list of [Built-in functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-functions-builtin) you can use for DBSQL.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Let's view all columns and 10 rows from the **aus_orders** table using the `LIMIT` statement. Notice that this table contains order information for individuals in Australia.

-- COMMAND ----------

SELECT *
FROM aus_orders
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Let's start our process by rearranging the order of the columns and renaming them by adding an **_** between words in the column names for readability. Run the query and view the results. Notice the column names have been modified.

-- COMMAND ----------

SELECT 
  orderid AS orders_id,
  customerid AS customer_id,
  productid AS product_id,
  quantity,
  orderamt AS order_amt,
  salesrep AS sales_rep,
  orderdate AS order_date
FROM aus_orders
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Create a column named **order_country** with the value *Australia* to indicate that all of these orders are from Australia. 
-- MAGIC
-- MAGIC     Run the query and view the **order_country** column. Notice that the column contains the value *Australia*.

-- COMMAND ----------

SELECT 
  orderid AS orders_id,
  customerid AS customer_id,
  productid AS product_id,
  quantity,
  orderamt AS order_amt,
  salesrep AS sales_rep,
  'Australia' AS order_country,        -- Create the order_country column
  orderdate AS order_date
FROM aus_orders
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Use the `UPPER` function to uppercase the values in the **salesrep** column to standardize the values in that column in case there are any case inconsistencies.
-- MAGIC
-- MAGIC     Run the query and view the **salesrep** column. Notice that all values have been uppercased.

-- COMMAND ----------

SELECT 
  orderid AS orders_id,
  customerid AS customer_id,
  productid AS product_id,
  quantity,
  orderamt AS order_amt,
  UPPER(salesrep) AS sales_rep,        -- Uppercase the values
  'Australia' AS order_country, 
  orderdate AS order_date
FROM aus_orders
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Create a column named **price_per_item** by dividing **order_amt** by **quantity** and rounding the result to two decimal places.
-- MAGIC
-- MAGIC     Run the query and view the results. Notice that the **price_per_item** column has been calculated.

-- COMMAND ----------

SELECT 
  orderid AS orders_id,
  customerid AS customer_id,
  productid AS product_id,
  quantity,
  orderamt AS order_amt,
  ROUND(order_amt/quantity, 2) AS price_per_item,          -- Calculate the price_per_item
  UPPER(salesrep) AS sales_rep,
  'Australia' AS order_country,
  orderdate AS order_date
FROM aus_orders
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 6. For detailed downstream analysis, it can be beneficial to parse out the **order_date** column into specific date values. Here, let's parse the **order_date** column into six columns for detailed analysis:
-- MAGIC
-- MAGIC    - **order_year** - [year function](https://docs.databricks.com/aws/en/sql/language-manual/functions/year)
-- MAGIC
-- MAGIC    - **order_month** - [month function](https://docs.databricks.com/aws/en/sql/language-manual/functions/month)
-- MAGIC
-- MAGIC    - **order_day** - [day function](https://docs.databricks.com/aws/en/sql/language-manual/functions/day)
-- MAGIC
-- MAGIC    - **order_dayofweek** - [dayname function](https://docs.databricks.com/aws/en/sql/language-manual/functions/dayname)
-- MAGIC
-- MAGIC    - **order_quarter** - [quarter function](https://docs.databricks.com/aws/en/sql/language-manual/functions/quarter)
-- MAGIC
-- MAGIC    - **order_year_quarter** - Concatenate the order year with the quarter (e.g., 2020Q1) using the [concat function](https://docs.databricks.com/aws/en/sql/language-manual/functions/concat)
-- MAGIC
-- MAGIC    - You can also use the [date_format function](https://docs.databricks.com/aws/en/sql/language-manual/functions/date_format) for additional date conversions.
-- MAGIC
-- MAGIC    Run the query and view the results. Notice all of the new **order_date** columns.
-- MAGIC
-- MAGIC

-- COMMAND ----------

SELECT 
  orderid AS orders_id,
  customerid AS customer_id,
  productid AS product_id,
  quantity,
  orderamt AS order_amt,
  ROUND(order_amt/quantity,2) AS price_per_item,
  UPPER(salesrep) AS sales_rep,
  'Australia' AS order_country,
  orderdate AS order_date,
  YEAR(order_date) AS order_year,                             -- Obtain the year
  MONTH(order_date) AS order_month,                           -- Obtain the month
  DAY(order_date) AS order_day,                               -- Obtain the day number
  DAYNAME(order_date) AS order_dayofweek,                     -- Obtain day of week as a string
  QUARTER(order_date) AS order_quarter,                       -- Obtain the quarter
  CONCAT(order_year,'-Q',order_quarter) AS order_year_quarter -- Create the year and quarter: 2020-Q1
FROM aus_orders
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 7. Let's create a column named **order_amt_category** that specifies if the order amount is *Low*, *Middle*, or *High* using the following values:
-- MAGIC    - **Low**: Less than or equal to 250,000
-- MAGIC    - **Middle**: Between 250,000 and 1,000,000
-- MAGIC    - **High**: Greater than or equal to 1,000,000
-- MAGIC
-- MAGIC To create the column, use a `CASE WHEN` expression (case expression). The `CASE WHEN` expression uses an expression to test for a condition. If the condition is true, it returns the specified value. Run the query and view the results. Notice that the new **order_amt_category** column was created with the specified values.
-- MAGIC
-- MAGIC [case expression](https://docs.databricks.com/aws/en/sql/language-manual/functions/case)

-- COMMAND ----------

SELECT 
  orderid AS orders_id,
  customerid AS customer_id,
  productid AS product_id,
  quantity,
  orderamt AS order_amt,
  ROUND(order_amt/quantity,2) AS price_per_item,
  UPPER(salesrep) AS sales_rep,
  'Australia' AS order_country,
  orderdate AS order_date,
  YEAR(order_date) AS order_year,                             
  MONTH(order_date) AS order_month,                           
  DAY(order_date) AS order_day,                              
  DAYNAME(order_date) AS order_dayofweek,                     
  QUARTER(order_date) AS order_quarter,                       
  CONCAT(order_year,'Q',order_quarter) AS order_year_quarter,
  -- Create a new column for order_amt_category based on these conditions
  CASE                                                    
    WHEN order_amt <= 250000 THEN 'Low'
    WHEN order_amt > 250000 AND order_amt < 1000000 THEN 'Middle'
    ELSE 'High'
  END AS order_amt_category
  -- End CASE WHEN statement
FROM aus_orders
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 8. Looking at the results from above, notice that we have the **product_id** for each order. 
-- MAGIC
-- MAGIC     However, that value does not tell us the specific product name. Our goal is to obtain the **product name** for each order to easily identify the product for our downstream analysis. We can do that using the **au_products_lookup** table.
-- MAGIC
-- MAGIC     Run the query below to view the **au_products_lookup** table. Notice that the table contains the **productid** and **productname** columns. We can use the **productid** column from both tables to perform a join to obtain the **productname** column.

-- COMMAND ----------

SELECT *
FROM au_products_lookup;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 9. Let's perform an INNER JOIN with the **au_products_lookup** table to obtain the **productname** column using the **productid** column from each table.
-- MAGIC
-- MAGIC     In the query below:
-- MAGIC     - The **aus_orders** table has the alias **ord**, which is added in front of the columns to explicitly pull those columns from the table.
-- MAGIC     - The **au_products_lookup** table has the alias **prod**, which is added in front of **productname** to select that column from the table.
-- MAGIC     - The join occurs on the **ord.productid** and the **prod.productid** columns.
-- MAGIC
-- MAGIC
-- MAGIC     **Summary of joins:**
-- MAGIC     - **INNER JOIN**: Returns only matching rows from both tables.
-- MAGIC     - **LEFT JOIN**: Returns all rows from the left table, and matching rows from the right table (null for non-matching).
-- MAGIC     - **RIGHT JOIN**: Returns all rows from the right table, and matching rows from the left table (null for non-matching).
-- MAGIC     - **FULL JOIN**: Returns all rows from both tables, with nulls where there is no match.
-- MAGIC
-- MAGIC     For more details, refer to the [Databricks JOIN documentation](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-join).

-- COMMAND ----------

SELECT 
  ord.orderid AS orders_id,
  ord.customerid AS customer_id,
  ord.productid AS product_id,
  prod.productname AS product_name,            -- Obtain the productname column from the au_products_lookup table
  ord.quantity,
  ord.orderamt AS order_amt,
  ROUND(order_amt/quantity,2) AS price_per_item,
  UPPER(salesrep) AS sales_rep,
  'Australia' AS order_country,
  ord.orderdate AS order_date,
  YEAR(order_date) AS order_year,                             
  MONTH(order_date) AS order_month,                         
  DAY(order_date) AS order_day,                               
  DAYNAME(order_date) AS order_dayofweek,                     
  QUARTER(order_date) AS order_quarter,                       
  CONCAT(order_year,'Q',order_quarter) AS order_year_quarter,
  CASE                                                    
    WHEN order_amt <= 250000 THEN 'Low'
    WHEN order_amt > 250000 AND order_amt < 1000000 THEN 'Middle'
    ELSE 'High'
  END AS order_amt_category
FROM aus_orders ord
  INNER JOIN au_products_lookup prod          -- INNER JOIN with the au_products_lookup table
  ON ord.productid = prod.productid           -- On the productid column in each table
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 10. Now that we have gone through the steps, let's put it all together with a `CREATE TABLE` statement to create the new table **aus_orders_silver** that prepares our data according to our objectives.
-- MAGIC
-- MAGIC     We will be using the medallion architecture during our data preparation. Remember, the medallion architecture is a data management approach that organizes data into multiple layers (bronze, silver, and gold) to progressively refine and enrich raw data for analytics and business intelligence.
-- MAGIC
-- MAGIC     - **Bronze** tables contain raw, unprocessed data directly ingested from source systems.
-- MAGIC
-- MAGIC     - **Silver** tables store cleaned and transformed data, typically with some level of aggregation and quality improvements for analysis.
-- MAGIC
-- MAGIC     - **Gold** tables hold high-quality, business-ready data, optimized for reporting and analytics, often containing final aggregations or metrics.
-- MAGIC
-- MAGIC
-- MAGIC ![Medallion Architecture](../Includes/images/medallion_architecture.png)

-- COMMAND ----------

-- Drop the table if it exists if running this cell multiple times during a demonstration
DROP TABLE IF EXISTS aus_orders_silver;


CREATE TABLE aus_orders_silver AS
SELECT 
  ord.orderid AS orders_id,
  ord.customerid AS customer_id,
  ord.productid AS product_id,
  prod.productname AS product_name,            -- Obtain the productname column from the au_products_lookup table
  ord.quantity,
  ord.orderamt AS order_amt,
  ROUND(order_amt/quantity,2) AS price_per_item,               -- Price per item calculation
  UPPER(salesrep) AS sales_rep,                                -- Upper case sales rep names
  'Australia' AS order_country,                                -- Country string
  ord.orderdate AS order_date,
  YEAR(order_date) AS order_year,                              -- Obtain the year
  MONTH(order_date) AS order_month,                            -- Obtain the month
  DAY(order_date) AS order_day,                                -- Obtain the month
  DAYNAME(order_date) AS order_dayofweek,                      -- Obtain day of week as a STRING
  QUARTER(order_date) AS order_quarter,                        -- Obtain the quarter
  CONCAT(order_year,'-Q',order_quarter) AS order_year_quarter, -- Create the year and quarter: 2020-Q1
  -- Create a new column for order_amt_category based on these conditions
  CASE                                                    
    WHEN order_amt <= 250000 THEN 'Low'
    WHEN order_amt > 250000 AND order_amt < 1000000 THEN 'Middle'
    ELSE 'High'
  END AS order_amt_category
  -- End CASE WHEN statement
FROM aus_orders ord
  INNER JOIN au_products_lookup prod           -- Join with the au_products_looup table
  ON ord.productid = prod.productid;           -- On productid

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 11. View the new **aus_orders_silver** table. Notice that it contains all of our new columns.

-- COMMAND ----------

SELECT *
FROM aus_orders_silver;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 12. Complete the following steps to view the lineage of the **aus_orders_silver** table using the Catalog Explorer:
-- MAGIC
-- MAGIC     a. In the left navigation bar, select the catalog icon ![catalog icon](../Includes/images/catalog_icon.png).  
-- MAGIC
-- MAGIC     b. Expand the **dbacademy** catalog.  
-- MAGIC
-- MAGIC     c. Expand your **labuser** schema.  
-- MAGIC
-- MAGIC     d. Expand **Tables**.  
-- MAGIC
-- MAGIC     e. Find the **aus_orders_silver** table you created, and to the right of the table, select the ellipsis ![ellipsis](../Includes/images/ellipsis.png).  
-- MAGIC
-- MAGIC     f. Select **Open in Catalog Explorer**.  
-- MAGIC
-- MAGIC     g. In the navigation bar, select **Lineage**. Here, you can see the **Upstream** tables.  
-- MAGIC
-- MAGIC     h. To view an interactive graph of the data lineage, click **See lineage graph**. By default, one level is displayed in the graph. Click the Plus Sign icon on a node to reveal more connections if they are available.  
-- MAGIC
-- MAGIC     i. Close the Catalog Explorer.
-- MAGIC
-- MAGIC
-- MAGIC <br></br>
-- MAGIC ![aus_orders_silver](../Includes/images/aus_orders_silver_lineage_image.png)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## D. Data Analysis
-- MAGIC Let's analyze the **aus_orders_silver** table and answer some basic business questions.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Begin by displaying the **aus_orders_silver** table and viewing 10 rows to preview the table.
-- MAGIC

-- COMMAND ----------

SELECT *
FROM aus_orders_silver
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D1. Filter
-- MAGIC Perform simple filtering and ordering using DBSQL.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. View all orders where:
-- MAGIC     - The **sales_rep** is *RAVI*.
-- MAGIC
-- MAGIC     - Orders are sorted by descending **order_amt**.

-- COMMAND ----------

SELECT
  sales_rep,
  orders_id,
  customer_id,
  product_name,
  order_amt,
  order_amt_category
FROM aus_orders_silver
WHERE sales_rep = 'RAVI'
ORDER BY order_amt DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. View all orders where:
-- MAGIC     - The **sales_rep** is *RAVI* AND the **customer_id** is *NS7598*.
-- MAGIC
-- MAGIC     - Orders are sorted by descending **order_amt**.

-- COMMAND ----------

SELECT
  sales_rep,
  orders_id,
  customer_id,
  product_name,
  order_amt,
  order_amt_category
FROM aus_orders_silver
WHERE sales_rep = 'RAVI' AND
      customer_id = 'NS7598'
ORDER BY order_amt DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D2. Simple Summary Statistics

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Count the total number of orders in the **aus_orders_silver** table. Run the query and view the results. Notice that we have 5,276 total orders.

-- COMMAND ----------

SELECT COUNT(*) AS total_orders
FROM aus_orders_silver

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Calculate the summary statistics for **order_amt**, including the **max**, **avg**, and **min** values. Run the query and view the results. 
-- MAGIC
-- MAGIC     Notice that we have a wide range of order amounts, with an average order amount of about *196,266*.

-- COMMAND ----------

SELECT
  max(order_amt) AS max_order_amount,
  avg(order_amt) AS avg_order_amount, 
  min(order_amt) AS min_order_amount
FROM aus_orders_silver

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D3. Aggregations and Visualizations

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Let's view the total **order_amt** for each **product_name** to see which product has the highest total order amount in the table and visualize the results.
-- MAGIC
-- MAGIC    Complete the following steps to run the query and create a visualization using the query results:
-- MAGIC
-- MAGIC       a. Run the cell below. Which product has the highest total order amount?
-- MAGIC
-- MAGIC       b. In the cell output, select the **+** icon.
-- MAGIC
-- MAGIC       c. Then select **Visualization**.
-- MAGIC
-- MAGIC       d. In the **General** tab, you can modify some basic options. Leave them at the default settings.
-- MAGIC
-- MAGIC       e. Select the **Y axis** tab and deselect **Sort Values**.
-- MAGIC
-- MAGIC       ![Y Axis Options](../Includes/images/yaxis_options_sort.png)
-- MAGIC
-- MAGIC       f. Select **Save**.
-- MAGIC
-- MAGIC       g. In the output cell below, double-click on **Visualization** and change the name to **Sales by Product**.
-- MAGIC
-- MAGIC       h. View the visualization you created. Notice how easy it is to create visualizations within Databricks.
-- MAGIC
-- MAGIC <br></br>
-- MAGIC **Final Visualization**
-- MAGIC ![Final Visualization](../Includes/images/final_visualization_order_by_product.png)

-- COMMAND ----------

SELECT 
  product_name, 
  ROUND(SUM(order_amt),2) as total_order_amount
FROM aus_orders_silver
GROUP BY product_name
ORDER BY total_order_amount DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Let's determine the total **order_amt** for each **product_name** broken down by **order_year_quarter** and visualize the results for each **product_name** on a line graph. 
-- MAGIC
-- MAGIC    Complete the following steps:
-- MAGIC
-- MAGIC    a. Run the cell below to calculate the results. Notice that we are using backticks in the query to clean up the column names for the visualization.
-- MAGIC
-- MAGIC     **NOTE:** You can also modify the labels within the **Visualization** UI.
-- MAGIC
-- MAGIC    b. In the cell output, select the **+** icon.
-- MAGIC
-- MAGIC    c. Then select **Visualization**.
-- MAGIC
-- MAGIC    d. In the **General** tab, you can modify some basic options. Change the **Visualization type** to **Line** and deselect **Horizontal chart**.
-- MAGIC    <img src="../Includes/images/year_order_general_options.png" width="600" alt="General Options">
-- MAGIC
-- MAGIC    e. Look at the visualization. Notice that the **Product Name** and **Year Quarter** labels are clean.
-- MAGIC
-- MAGIC    f. Select the **Y Axis** tab. This is where you can modify the amount label. Under the **Name** option, enter *Total Amount Sold* to clean up the Y axis label.
-- MAGIC    <img src="../Includes/images/year_order_y_axis_label.png" width="600" alt="Y Axis Label">
-- MAGIC
-- MAGIC    g. Select **Save**. Notice that the visualization was created.
-- MAGIC
-- MAGIC    h. Using your cursor, hover over the visualization. Notice that it is interactive.
-- MAGIC
-- MAGIC
-- MAGIC    <br></br>
-- MAGIC    **Final Visualization**
-- MAGIC    ![Final Visualization](../Includes/images/final_visualization_yearquarter_totalsold_product_name.png)

-- COMMAND ----------

SELECT 
  order_year_quarter AS `Year Quarter`,
  product_name AS `Product Name`, 
  ROUND(SUM(order_amt),2) AS `Total Amount Sold`
FROM aus_orders_silver
GROUP BY 
  order_year_quarter,
  product_name
ORDER BY order_year_quarter, product_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Let's determine the total sales amount for each sales representative, and what percentage of the total company sales each sales representative contributes.
-- MAGIC
-- MAGIC     To solve this, we will complete the following:
-- MAGIC
-- MAGIC     - In the `SELECT` clause, we will calculate the percentage of each sales rep's contribution by dividing the sales representative's total sales (**total_sales**) by the total sales of the entire company using `SELECT SUM(order_amt) FROM aus_orders_silver`.
-- MAGIC
-- MAGIC     - Use a `GROUP BY` clause with a `SUM` aggregation to calculate the **total_sales** for each **sales_rep**.
-- MAGIC
-- MAGIC     Run the query and view the results. Notice that the **percentage_of_sales** column contains the total percentage of sales for each sales representative.

-- COMMAND ----------

SELECT 
  sales_rep,
  ROUND(SUM(order_amt),2) as sales_rep_total_sales,
  ROUND(sales_rep_total_sales / (SELECT SUM(order_amt) FROM aus_orders_silver),2) as percentage_of_sales
FROM aus_orders_silver
GROUP BY sales_rep
ORDER BY percentage_of_sales DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D4. Common Table Expression (CTE)
-- MAGIC CTEs define a temporary result set that you can reference multiple times within the scope of a SQL statement. Depending on the query you are performing, they can help make your query more readable, easier to debug, and maintain.
-- MAGIC
-- MAGIC Let's rewrite the code from the previous step using a simple CTE.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. First, let's write the query to calculate the total amount of sales. Notice that the result returns one row with a single column showing the total sales: 1,035,503,255.36.

-- COMMAND ----------

SELECT ROUND(SUM(order_amt),2) AS total
FROM aus_orders_silver

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Next, let's incorporate the query from above into a CTE to separate the subquery within the `SELECT` clause that we used to calculate the percentage of sales for each sales rep.
-- MAGIC
-- MAGIC     The query below:
-- MAGIC
-- MAGIC     - Uses the `WITH` clause to create a temporary result set named **TotalSalesQry** that calculates the total sales across all orders using the query from above.
-- MAGIC
-- MAGIC     - In the main query, we then reference the **TotalSales** result (total sum of orders) within the `SELECT` clause using the statement: `ROUND(sales_rep_total_sales / (SELECT total FROM TotalSalesQry), 2) AS percentage_of_sales`.
-- MAGIC
-- MAGIC     Run the cell and view the results. Notice that the results are the same.
-- MAGIC
-- MAGIC     **NOTE:** For this simple example, a CTE might not be necessary, but CTEs can be much more complex and help modularize your query, making it more readable and easier to debug.

-- COMMAND ----------

-- CTE to store the total sales
WITH TotalSalesQry AS (
  SELECT ROUND(SUM(order_amt),2) AS total
  FROM aus_orders_silver
)
-- Query that uses the TotalSales CTE
SELECT 
    sales_rep,
    ROUND(SUM(order_amt), 2) AS sales_rep_total_sales,
    -- Use the CTE TotalSales from above
    ROUND(sales_rep_total_sales / (SELECT total FROM TotalSalesQry), 2) AS percentage_of_sales
FROM aus_orders_silver
GROUP BY sales_rep
ORDER BY percentage_of_sales DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D5. PIVOT
-- MAGIC What if you want to restructure your data? Within SQL the PIVOT operator is used to transform rows into columns, allowing you to reorganize and summarize data for easier analysis and reporting. 
-- MAGIC
-- MAGIC For example, what if we want to summarize the total sales of each **sales_rep** by **order_year** in the following format:
-- MAGIC | sales_rep | 2021        | 2022        | 2023        | 2024        |
-- MAGIC |-----------|-------------|-------------|-------------|-------------|
-- MAGIC | HARRY     | 1,894,401.56 | 14,919,971.27 | 19,191,059.66 | 13,700,168.75 |
-- MAGIC | ZURI      | 4,824,302.84 | 33,586,531.28 | 62,555,959.30 | 61,231,945.73 |
-- MAGIC | LESLIE    | 4,715,409.51 | 41,244,100.17 | 47,641,618.74 | 55,997,979.40 |
-- MAGIC | RAVI      | 5,436,493.42 | 90,624,752.06 | 92,317,450.30 | 100,601,239.93 |
-- MAGIC | RÓISÍN    | 4,698,899.42 | 94,268,067.91 | 100,327,746.54 | 115,555,931.50 |
-- MAGIC | LIAM      | 1,369,265.15 | 16,312,696.91 | 19,054,808.61 | 33,432,455.40 |
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Let's start by querying the columns in the **aus_orders_silver** table that we want to pivot. Notice that we have the **sales_rep**, **order_amt** and **order_year** columns.

-- COMMAND ----------

SELECT
    sales_rep, 
    order_amt, 
    order_year
FROM aus_orders_silver

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Now let's pivot the result set with a CTE and the `PIVOT` operator to restructure the table. 
-- MAGIC
-- MAGIC     In the following cell, the `PIVOT` operation uses:
-- MAGIC
-- MAGIC     - The `ROUND(SUM(order_amt))` statement to round and sum the **order_amt** column for each **sales_rep**.
-- MAGIC
-- MAGIC     - The `FOR order_year IN (2021, 2022, 2023, 2024)` statement pivots the data by transforming the **order_year** values into separate columns for each year: *2021, 2022, 2023, 2024*.
-- MAGIC
-- MAGIC
-- MAGIC **NOTE:** While not required, the CTE helps make the code more readable.

-- COMMAND ----------

-- Create CTE of the source table to pivot
WITH SourceTable AS (
    SELECT
        sales_rep, 
        order_amt, 
        order_year
    FROM 
        aus_orders_silver
)
-- Select all from the source table (CTE) and pivots the order_year column
SELECT *
FROM SourceTable
PIVOT (
    ROUND(SUM(order_amt),2)
    FOR order_year IN (2021, 2022, 2023, 2024)
)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Let's complete the same task without using the CTE. Each method will produce the same results.

-- COMMAND ----------

SELECT *
FROM (
    SELECT 
        sales_rep, 
        order_amt, 
        order_year
    FROM 
        aus_orders_silver
) AS SourceTable
PIVOT (
    ROUND(SUM(order_amt),2)
    FOR order_year IN (2021, 2022, 2023, 2024)
)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### D6. Windowing Functions
-- MAGIC Windowing functions in SQL allow you to perform calculations across a set of rows related to the current row, without collapsing the result set. They are used with the `OVER` clause to define a window of rows, enabling operations like:
-- MAGIC - ranking
-- MAGIC - running totals
-- MAGIC - moving averages within a specified range of data
-- MAGIC - and more
-- MAGIC
-- MAGIC Our goal is to view the top 3 sales amounts for each **sales_rep**.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Preview the **sales_rep** and **order_amt** columns in the **aus_orders_silver** table.
-- MAGIC
-- MAGIC     Run the query and view the results. Notice the following:
-- MAGIC       - In row 1, **sales_rep** *HARRY* has their largest order of *2466504.04*.
-- MAGIC       - In row 277, **sales_rep** *LESLIE* has their largest order of *3363380.3*.

-- COMMAND ----------

SELECT 
    sales_rep, 
    order_amt
FROM aus_orders_silver
ORDER BY sales_rep, order_amt DESC
LIMIT 500;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. The following cell uses a windowing function to rank the **order_amt** for each **sales_rep**.
-- MAGIC
-- MAGIC     - The `RANK()` function ranks each record within the specified partition (**sales_rep**).
-- MAGIC
-- MAGIC     - The `OVER` keyword is used with window functions to define the window for the function to operate on. It specifies how to partition and/or order the data.
-- MAGIC
-- MAGIC     - The `PARTITION BY` clause divides the data into groups by **sales_rep**.
-- MAGIC
-- MAGIC     - The `ORDER BY` clause orders the rows by descending **order_amt**.
-- MAGIC
-- MAGIC       Run the cell and view the results. Notice the following:
-- MAGIC         - Starting at row 1, you can see the **sale_rank** of **sales_rep** *HARRY*.
-- MAGIC         - Starting at row 277, the ranking resets for the new **sales_rep** *LESLIE*.
-- MAGIC
-- MAGIC     [Window functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-window-functions)

-- COMMAND ----------

SELECT 
    sales_rep, 
    order_amt,
    RANK() OVER(PARTITION BY sales_rep ORDER BY order_amt DESC) AS sale_rank
FROM aus_orders_silver

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Lastly, we want to filter for the top 3 greatest sales. To do that, you can use the `QUALIFY` clause. The `QUALIFY` clause is used in SQL to filter the results of window functions, like `RANK()`, after they have been calculated.
-- MAGIC
-- MAGIC     Run the cell and view the results. Notice that we can see the top three **sale_rank** for each **sales_rep**.
-- MAGIC
-- MAGIC     [QUALIFY clause](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-qualify)
-- MAGIC
-- MAGIC     **NOTE:** You can't use the `WHERE` clause to filter a column created by window function.

-- COMMAND ----------

SELECT 
  sales_rep, 
  order_amt,
  RANK() OVER (PARTITION BY sales_rep ORDER BY order_amt DESC) AS sale_rank
FROM aus_orders_silver
QUALIFY sale_rank <=3;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Additional Resources
-- MAGIC
-- MAGIC - [Built-in functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-functions-builtin)
-- MAGIC
-- MAGIC - [What are user-defined functions (UDFs)?](https://docs.databricks.com/aws/en/udf/)
-- MAGIC
-- MAGIC - [Window functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-window-functions)
-- MAGIC
-- MAGIC - [CREATE FUNCTION (SQL and Python)](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-sql-function)
-- MAGIC
-- MAGIC - [Apply AI on data using Databricks AI Functions](https://docs.databricks.com/aws/en/large-language-models/ai-functions) - Public Preview as of 2025Q1

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
