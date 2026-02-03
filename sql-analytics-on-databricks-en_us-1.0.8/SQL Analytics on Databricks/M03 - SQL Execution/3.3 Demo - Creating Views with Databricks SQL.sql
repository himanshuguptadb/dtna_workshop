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
-- MAGIC # 3.3 Demo - Creating Views with Databricks SQL
-- MAGIC
-- MAGIC In this demonstration, we will explore various types of views in Databricks and their applications. First, we will create a standard view and analyze its behavior, followed by constructing a temporary view and evaluating its session-based usage. Next, we will develop a materialized view to assess its impact on query performance, and finally, we will build a dynamic view to examine how it handles real-time data updates for continuous querying.
-- MAGIC
-- MAGIC ### Objectives
-- MAGIC - Create a standard view and analyze its behavior to understand how it is defined, stored, and queried in Databricks.
-- MAGIC - Create a temporary view and evaluate its purpose in session-based data processing, learning how it differs from standard views.
-- MAGIC - Create a materialized view and assess its performance by storing precomputed results and reducing query computation time.
-- MAGIC - Create a dynamic view and examine how it handles real-time data, enabling continuous updates for queries in Databricks.

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

-- MAGIC %run ../Includes/3.3-Classroom-Setup

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
-- MAGIC Create a sample table named **employees** with 5 rows and 3 columns to use in the demonstration.

-- COMMAND ----------

-- Drop the table if it already exists to start from the beginning
DROP TABLE IF EXISTS employees;

-- Create the employees table
CREATE TABLE employees (
    EmployeeID INT,
    FirstName VARCHAR(20),
    Department VARCHAR(20)
);

-- Insert 5 rows of sample data
INSERT INTO Employees (EmployeeID, FirstName, Department)
VALUES
(1, 'John', 'Marketing'),
(2, 'Raul', 'HR'),
(3, 'Michael', 'IT'),
(4, 'Panagiotis', 'Finance'),
(5, 'Aniket', 'Operations');

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Run the query and view the **employees** table. Confirm that it contains 3 columns and 5 rows, with **EmployeeID** values from 1 to 5.

-- COMMAND ----------

SELECT *
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## B. Introduction to View Types in Databricks SQL
-- MAGIC - B1. Standard Views
-- MAGIC - B2. Temporary Views
-- MAGIC - B3. Materialized Views
-- MAGIC - B4. Dynamic Views

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B1. Standard View
-- MAGIC
-- MAGIC
-- MAGIC A **standard view** is essentially a saved query in the database. It doesn't store any data physically but rather defines a query that is executed every time you access the view.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Use the `CREATE OR REPLACE VIEW` statement to create a simple standard view named **employees_vw**. Remember, a standard view stores the text of a query within the view name.
-- MAGIC
-- MAGIC     In this example, the view will simply query all rows from the **employees** table and create the new column **ViewType** with the value *Standard View* when executed. 
-- MAGIC
-- MAGIC     Run the code and view the results. Notice that the view is created successfully.

-- COMMAND ----------

CREATE OR REPLACE VIEW employees_vw AS
SELECT 
  *, 
  'Standard View' AS ViewType
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Run the `SHOW TABLES` to view all tables in your **labuser** schema. Notice that your **employees_vw** is shown in the table list even though it is a view, not a table.

-- COMMAND ----------

SHOW TABLES;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Use the `SHOW VIEWS` statement to display only the views in your **labuser** schema. Notice that it returns the following about the view(s):
-- MAGIC
-- MAGIC     - **namespace** - The catalog name
-- MAGIC
-- MAGIC     - **viewName** - The name of the view.
-- MAGIC
-- MAGIC     - **isTemporary** - If the view is temporary
-- MAGIC
-- MAGIC     - **isMaterialized** - If the view is a materialized view.
-- MAGIC
-- MAGIC
-- MAGIC     In this example, the **employees_vw** is a standard view, it is not temporary, and is not materialized.

-- COMMAND ----------

SHOW VIEWS;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Describe the **employees_vw** view. Scroll to the bottom and notice that there are additional view information rows. Explore the following rows under the *#Detailed Table Information* section:
-- MAGIC
-- MAGIC     - **Type**: Displays the type of the view.
-- MAGIC
-- MAGIC     - **View Text**: The query text of the view.
-- MAGIC     - **View Query Output Columns**: The output columns created by the view.

-- COMMAND ----------

DESCRIBE TABLE EXTENDED employees_vw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Run a query on the view **employees_vw**. 
-- MAGIC
-- MAGIC     When querying a view it will run the stored query text every single time the view is queried. In this example it is a simple view that queries all rows from the **employees** table and adds the column **ViewType**.
-- MAGIC     <br></br>
-- MAGIC     ```SQL
-- MAGIC     SELECT *, 'Standard View' AS ViewType 
-- MAGIC     FROM employees
-- MAGIC     ```
-- MAGIC
-- MAGIC **NOTE:** If the query the view has stored is resource intensive, this can cause performance issues if you are referencing the standard view multiple times throughout your code since it will execute the stored query each time. In this example the table is small and performance will not be an issue.

-- COMMAND ----------

SELECT * 
FROM employees_vw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 6. Insert another row into the original **employees** table. The new row will contain a new employee with **EmployeeID** 6.

-- COMMAND ----------

INSERT INTO employees (EmployeeID, FirstName, Department)
VALUES
(6, 'Athena', 'Marketing');

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 7. Query the **employees_vw**. The view will execute the stored query and obtain the most up to date data in the **employees** and create the additional **ViewType** column.

-- COMMAND ----------

SELECT * 
FROM employees_vw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Standard View Summary 
-- MAGIC ##### Benefits:
-- MAGIC
-- MAGIC - **On-Demand Queries**: Use a standard view when the data is relatively small, the query runs quickly, and you want the most up-to-date data each time you run the query.
-- MAGIC
-- MAGIC - **\*View Persists**: Saves the standard view to a catalog and schema, and the view can be shared among other users.
-- MAGIC
-- MAGIC - **Fresh Data**: When you want to always access the most up-to-date data from the underlying tables.
-- MAGIC
-- MAGIC - **Low Storage Requirements**: Since views don’t store data, views don’t require any additional storage.
-- MAGIC
-- MAGIC ##### Considerations:
-- MAGIC - **Performance**: Every time the view is queried, the **underlying query has to be executed**, which can be slow if the data volume is large or the query is complex.
-- MAGIC
-- MAGIC - **\*View Persists**: Saves the view to a catalog and schema, so if you only need the view temporarily for your current session, you are still saving it to your schema as an object.
-- MAGIC
-- MAGIC - **No Caching**: Standard views don't benefit from caching, so each execution of the view re-computes the query.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B2. Temporary Views
-- MAGIC
-- MAGIC A **temporary view** is similar to a standard view in that it represents a query result. However, the key difference is that temporary views only exist for the duration of the session or notebook. They are useful for short-lived queries or exploratory data analysis where you don't need to save the view. 
-- MAGIC
-- MAGIC There are two types of temporary views:
-- MAGIC
-- MAGIC - **TEMPORARY** - views are visible only to the session that created them and are dropped when the session ends.
-- MAGIC
-- MAGIC - **GLOBAL TEMPORARY** - views are tied to a system preserved temporary schema global_temp. 
-- MAGIC
-- MAGIC   - **NOTE:** Global temporary views are not supported on a SQL warehouse.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Query the **employees** table and confirm that the table contains 6 rows and 3 columns.

-- COMMAND ----------

SELECT *
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Use the `CREATE OR REPLACE TEMPORARY VIEW` statement to create a temporary view named **employees_temp_vw**.
-- MAGIC
-- MAGIC     The temporary view will query all rows from the **employees** table and create a new column named **ViewType** with the value *Temp View*.

-- COMMAND ----------

CREATE OR REPLACE TEMPORARY VIEW employees_temp_vw AS
SELECT 
  *, 
  'Temp View' AS ViewType
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Run the `SHOW VIEWS` statement to view available views in your **labuser** schema.
-- MAGIC
-- MAGIC     Notice the following for **employees_temp_vw**:
-- MAGIC     - The temporary view does not have a **namespace** value since it is temporary.
-- MAGIC     - The temporary view has a *true* value for the **isTemporary** column.
-- MAGIC     - The temporary view has a value of *false* for **isMaterialized**.
-- MAGIC
-- MAGIC **NOTES:** 
-- MAGIC - If the SQL warehouse terminates, or you detach and reattach to the cluster, the temporary view will be cleared.
-- MAGIC - If you open another notebook, the temporary view will not be available in that session.

-- COMMAND ----------

SHOW VIEWS;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Query the temporary view **employees_temp_vw** and notice that it returns all 6 employees with the new column **ViewType**.

-- COMMAND ----------

SELECT *
FROM employees_temp_vw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Let's add another row (**EmployeeID** 7) to the original **employees** table and view the table. Confirm that the **employees** table contains 7 rows and 3 columns.

-- COMMAND ----------

INSERT INTO employees (EmployeeID, FirstName, Department)
VALUES
(7, 'Pedro', 'Training');

SELECT *
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 6. What do you think will happen when we rerun the temporary view? Will it:
-- MAGIC
-- MAGIC    - Only return the original 6 rows of data when the temporary view was created?
-- MAGIC
-- MAGIC    - Or will it recompute and get the most up to date data (7 rows)?
-- MAGIC
-- MAGIC    Run the query and view the results. Notice that when the temporary view is executed, it obtains the most up to date data because it executes the query stored in the temporary view.

-- COMMAND ----------

SELECT *
FROM employees_temp_vw

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Temporary View Summary
-- MAGIC
-- MAGIC ##### Benefits:
-- MAGIC
-- MAGIC - **\*View Does Not Persist**: Temporary views are not stored in the schema, so once the session ends, they are dropped automatically. These are great if you only need the view for your session.
-- MAGIC
-- MAGIC - **Exploratory Data Analysis** Great for (EDA) where you want to quickly test or inspect different transformations or aggregations without the need to store them permanently.
-- MAGIC
-- MAGIC - **Intermediary Results**: Great when you need to store intermediate results temporarily while performing multiple steps of a complex computation, without the need to persist the data.
-- MAGIC
-- MAGIC - **Sharing Within a Session**: Great when you want to make the share the query available across multiple queries within the same session.
-- MAGIC
-- MAGIC ##### Considerations:
-- MAGIC
-- MAGIC - **Session-Specific**: Temporary views are session-specific, which means they cannot be accessed by other users or sessions.
-- MAGIC
-- MAGIC - **\*View Does Not Persist**: Temporary views are not stored in the schema, so once the session ends, they are dropped automatically.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B3. Materialized Views
-- MAGIC
-- MAGIC A **materialized view** are Unity Catalog managed tables that allow users to precompute results based on the latest version of data in source tables. Materialized views CAN be updated periodically (or on demand) based on a refresh mechanism to get the most up to date data.
-- MAGIC
-- MAGIC Materialized views on Databricks differ from other implementations as the results returned reflect the state of data when the materialized view was last refreshed rather than always updating results when the materialized view is queried. You can manually refresh materialized views or schedule refreshes.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Use the `CREATE OR REPLACE MATERIALIZED VIEW` statement to create the materialized view.
-- MAGIC
-- MAGIC    In Databricks SQL, materialized views are Unity Catalog managed tables that allow users to precompute results based on the latest version of data in source tables. Each time a materialized view is refreshed, query results are recalculated to reflect changes in upstream datasets.
-- MAGIC
-- MAGIC    Run the cell below and view the results. Notice that the output returns *The operation was successfully executed*.
-- MAGIC
-- MAGIC    **NOTES:** 
-- MAGIC    - This cell will take about a minute to complete.
-- MAGIC    - Materialized views created in Databricks SQL are backed by a serverless DLT pipeline. Your workspace must support serverless pipelines to use this functionality.
-- MAGIC    - For more information view the [Use materialized views in Databricks SQL](https://docs.databricks.com/aws/en/views/materialized). This demonstration will quickly overview a materialized view.

-- COMMAND ----------

CREATE OR REPLACE MATERIALIZED VIEW employees_mv AS
SELECT 
  *,
  'Materialized View' AS ViewType
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Complete the following to use the UI to display the view objects in your schema.
-- MAGIC
-- MAGIC    a. In the left navigation bar, select the catalog icon ![Catalog Icon](../Includes/images/catalog_icon.png)
-- MAGIC
-- MAGIC    b. Expand the **dbacademy** catalog.
-- MAGIC
-- MAGIC    c. Expand your **labuser** schema.
-- MAGIC
-- MAGIC    d. Expand **Tables**.
-- MAGIC
-- MAGIC    e. Scroll down and find the **employees_mv** and **employees_vw** views. Look at the icons. Notice that:
-- MAGIC
-- MAGIC       - A materialized view is stored in your schema.
-- MAGIC
-- MAGIC       - The icons differ for a materialized view (**employees_mv**) and a standard view (**employees_vw**).
-- MAGIC
-- MAGIC    ![View Icons](../Includes/images/mv_vs_view_icons.png)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Run the `SHOW VIEWS` statement to view available views in your **labuser** schema.
-- MAGIC
-- MAGIC    Notice the following for the materialized view **employees_mv**:
-- MAGIC    - The materialized view has been stored in your **labuser** **namespace**.
-- MAGIC    - The materialized view has a *false* value for the **isTemporary** column.
-- MAGIC    - The materialized view has a value of *true* for **isMaterialized**.

-- COMMAND ----------

SHOW VIEWS;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Select all rows from the **employees_mv** materialized view. Run the cell and view the results. Notice that the materialized view returns 7 rows and 4 columns.

-- COMMAND ----------

SELECT *
FROM employees_mv;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. Insert a new row into the **employees** table with the **EmployeeID** of 8. Run the cell and view the results. Notice that the **employees** table now has 8 rows and 3 columns.

-- COMMAND ----------

INSERT INTO employees (EmployeeID, FirstName, Department)
VALUES
(8, 'Dimitri', 'IT');

SELECT *
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 6. Select all rows from the materialized view **employees_mv**. Before you run the cell, how many rows do you think the view will display? 
-- MAGIC
-- MAGIC       - The original 7 rows in the **employees** table when the materialized view was created?
-- MAGIC
-- MAGIC       - Or the current 8 rows in the **employee** table?
-- MAGIC
-- MAGIC    Run the cell and view the results. Notice that the materialized view displays the 7 rows of data that were present in the **employees** table when the materialized view was created. This is because it precomputes the results and stores them as an object to avoid recomputing the results each time the materialized view is executed.
-- MAGIC
-- MAGIC    **NOTE:** Using a materialized view is much more efficient than a standard or temporary view when the view is resource-intensive. This is because each time a standard view or temporary view is used, the results must be computed. The drawback is that a materialized view must be refreshed to get the most up-to-date data.

-- COMMAND ----------

SELECT *
FROM employees_mv;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 7. To get the most up-to-date data from the **employees** table, you must refresh the materialized view. You can do that using the `REFRESH MATERIALIZED VIEW` statement.
-- MAGIC
-- MAGIC    Run the cell and view the results. This will refresh the data for the materialized view to get the most up-to-date data from the **employees** table.
-- MAGIC
-- MAGIC     [REFRESH (MATERIALIZED VIEW or STREAMING TABLE documentation)](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-refresh-full)

-- COMMAND ----------

REFRESH MATERIALIZED VIEW employees_mv;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 8. Select all rows from the refreshed **employees_mv** materialized view. Run the cell and view the results. How many rows do you think will be displayed, 7 or 8?
-- MAGIC
-- MAGIC    Run the cell and view the results. Notice that after the materialized view was refreshed, we now have the updated data from the **employees** table (all 8 rows).

-- COMMAND ----------

SELECT *
FROM employees_mv;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 9. Instead of manually refreshing a materialized view, you can schedule a refresh when creating it. 
-- MAGIC
-- MAGIC
-- MAGIC     For example, if you want to schedule the materialized view to be refreshed every hour, you can use the `SCHEDULE EVERY` statement when creating the materialized view.
-- MAGIC
-- MAGIC     For more information, refer to the [CREATE MATERIALIZED VIEW statement documentation](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-materialized-view).

-- COMMAND ----------

CREATE OR REPLACE MATERIALIZED VIEW employees_mv_scheduled
  SCHEDULE EVERY 1 HOUR       -- Schedule when to refresh the view.
AS
SELECT 
  *,
  'Materialized View' AS ViewType
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 10. Use the `DESCRIBE EXTENDED` statement to describe the scheduled materialized view **employees_mv_scheduled**. Run the cell and view the results. In the results, scroll to the bottom and find the **# Refresh Information**. 
-- MAGIC
-- MAGIC
-- MAGIC       Notice the following:
-- MAGIC
-- MAGIC       - Under **Refresh Information**, you can see that this materialized view is scheduled for refresh (or has been refreshed).
-- MAGIC       - You can see refresh information such as **Last Refreshed, Last Refresh Type, Latest Refresh Status, and Latest Refresh**.
-- MAGIC       - The row **Refresh Schedule** indicates how often this materialized view is refreshed. In this example, it's every 1 hour.

-- COMMAND ----------

DESCRIBE EXTENDED employees_mv_scheduled;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Materialized Views Summary
-- MAGIC
-- MAGIC ##### Benefits:
-- MAGIC
-- MAGIC - **Performance Optimizations**: When the underlying query is computationally expensive and you want to precompute and store the results, so querying the view is faster in your code.
-- MAGIC
-- MAGIC - **Latest Data Not Required**: When the data in the view doesn't need to be updated in real-time but should be refreshed periodically (e.g., daily or hourly).
-- MAGIC
-- MAGIC - **Data Aggregation**: If the view is an aggregate (e.g., summaries, averages, counts), and recalculating these aggregates is time consuming, materialized views can store the precomputed results.
-- MAGIC
-- MAGIC
-- MAGIC ##### Considerations:
-- MAGIC
-- MAGIC - **Storage**: Materialized views take up storage, as they store the results of the query in your schema.
-- MAGIC
-- MAGIC - **Data Staleness**: The data can become stale depending on the refresh interval. If your underlying data changes frequently and you need real-time data, materialized views might not be ideal.
-- MAGIC
-- MAGIC - **Maintenance**: You need to manage the refresh strategy for the materialized view, which may include full or incremental refreshes.
-- MAGIC
-- MAGIC For more information, check out [Use materialized views in Databricks SQL](https://docs.databricks.com/aws/en/views/materialized).

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B4. Dynamic Views
-- MAGIC
-- MAGIC In Unity Catalog, you can use **dynamic views** to configure fine-grained access control, including:
-- MAGIC - Column level security
-- MAGIC - Row level security
-- MAGIC - Data masking (not covered in this demonstration)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Start by using the `is_account_group_member` function to check if you are a member of the **admins** group. Run the cell and view the results. Notice that it returns the value *false*, indicating that you are not part of the **admins** group.

-- COMMAND ----------

SELECT is_account_group_member('admins');

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Query the **employees** table and confirm the table contains 8 rows and the columns **EmployeeID, FirstName and Department**.

-- COMMAND ----------

SELECT *
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. With a dynamic view, you can limit the columns a specific user or group can access. In the following example, only members of the **admins** group can access the **FirstName** column from the **employees** table. 
-- MAGIC
-- MAGIC     To add column-level permission in query, use the CASE statement to replace with the literal string value *Redacted* or the actual contents of the **FirstName** column based on if the user executing the query is in the **admins** group.

-- COMMAND ----------

CREATE OR REPLACE VIEW employees_redact_name_col_dynamic_vw AS
SELECT
  EmployeeID,
  -- Redact a column when not part of the 'admins' group
  CASE WHEN 
    -- When you are part of the 'admins' group (true), return the FirstName       
    is_account_group_member('admins') THEN FirstName
    -- If not part of the 'admins' group (false), you can't see the FirstName and see 'Redacted'    
    ELSE 'Redacted'                                     
  END AS FirstName,
  Department
FROM employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Query the **employees_redact_name_col_dynamic_vw** view. Before you run the query, what do you think will happen? Remember, you are not part of the **admins** group.
-- MAGIC
-- MAGIC     Run the cell and view the results. Notice that since you are not part of the **admins** group, you can't see the employee's **FirstName**. 
-- MAGIC
-- MAGIC     **NOTES:** With dynamic views, you can limit the columns accessible to specific users or groups, which enables you to share this view with others and based on their access, they can see (or not see) specific columns.

-- COMMAND ----------

SELECT *
FROM employees_redact_name_col_dynamic_vw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 5. With a dynamic view, you can also specify permissions down to the row level. In the following example, only members of the **admins** group can view all employees. If you are not part of the **admin** group you can only view the employees in the *IT* **Department**. 
-- MAGIC
-- MAGIC     Run the cell below and view the results. Recall you are not part of the **admins** group, so you only can access the rows where **Department** is *IT*.

-- COMMAND ----------

CREATE OR REPLACE VIEW employees_filter_dynamic_vw AS
SELECT * 
FROM employees
WHERE
  -- Dynamic view to filter on the Department column
  CASE
    -- When a member of the admins group (true), you can see all rows
    WHEN is_account_group_member('admins') THEN TRUE
    -- Otherwise not part of the admins group (false), you can only see the IT rows
    ELSE Department = 'IT'
  END;



-- Display the view
SELECT *
FROM employees_filter_dynamic_vw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Dynamic Views Summary
-- MAGIC
-- MAGIC ##### Benefits:
-- MAGIC - **Access Control**: Can use dynamic views to configure fine-grained access control.
-- MAGIC
-- MAGIC
-- MAGIC ##### Considerations:
-- MAGIC - **Compatibility**: Dynamic views may not be supported across all Databricks environments or configurations. View the [Before you begin](https://docs.databricks.com/aws/en/views/dynamic#before-you-begin) documentation.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## C. Explore Views Using the Information Schema
-- MAGIC The **INFORMATION_SCHEMA** is a SQL standard based schema, provided in every catalog created on Unity Catalog. Within the information schema, you can find a set of views describing the objects known to the schema’s catalog that you are privileged to see.
-- MAGIC
-- MAGIC
-- MAGIC For this demonstration, let's explore the **views** view within the **information_schema** in your **dbacademy** catalog to explore the views that have been created.
-- MAGIC
-- MAGIC **NOTES:**
-- MAGIC
-- MAGIC - [Information schema](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-information-schema) documentation
-- MAGIC
-- MAGIC - Information schema [VIEWS](https://docs.databricks.com/aws/en/sql/language-manual/information-schema/views) documentation

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 1. Run the cell below to view the value of the `DA.schema_name` SQL variable that was created for you during the classroom setup script that simply stores your schema name in an SQL variable. Confirm it returns your **labuser** name (example, labuser1234_5678).

-- COMMAND ----------

values(DA.schema_name)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 2. Query the **dbacademy.information_schema.views** view and look at the results. 
-- MAGIC
-- MAGIC     Notice that it:
-- MAGIC     - Displays all of the views available to you, including the **information_schema** views.
-- MAGIC     - The **table_schema** column contains the schema of the view.

-- COMMAND ----------

SELECT *
FROM dbacademy.information_schema.views;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 3. Filter the **table_schema** column using the `WHERE` clause to filter all of the views within your **labuser** schema using the `DA.schema_name` variable we saw earlier. Run the query and view the results. Notice that:
-- MAGIC
-- MAGIC     - You can see information about the views we created in the demonstration (**employees_vw**, **employees_mv**, **employees_mv_scheduled**, and **employees_dynamic_vw**).
-- MAGIC
-- MAGIC     - The **view_definition** column displays the query the view holds.
-- MAGIC
-- MAGIC     - The **is_materialized** column (the last column on the right) indicates if the view is materialized.

-- COMMAND ----------

SELECT *
FROM dbacademy.information_schema.views
WHERE table_schema = DA.schema_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Additional Resources
-- MAGIC
-- MAGIC - [What is a view?](https://docs.databricks.com/aws/en/views/)
-- MAGIC
-- MAGIC - [Materialized Views](https://www.databricks.com/glossary/materialized-views)
-- MAGIC
-- MAGIC - [Create a dynamic view](https://docs.databricks.com/aws/en/views/dynamic)
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
