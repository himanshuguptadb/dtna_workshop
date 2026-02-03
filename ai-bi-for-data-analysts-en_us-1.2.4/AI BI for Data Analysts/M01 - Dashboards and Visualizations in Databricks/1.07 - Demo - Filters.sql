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
-- MAGIC ## 1.07 Demo - Filters
-- MAGIC
-- MAGIC Databricks AI/BI Dashboards help you quickly transform data into shareable insights. 
-- MAGIC
-- MAGIC In this lesson, we’ll learn about the capabilities of AI/BI Dashboards to let your Dashboard's end users interact with your dashboards. These features make both them and you more productive. They help your users be more self-sufficient, and they free up your time from having to handle as many one-off requests for new dashboard features.
-- MAGIC
-- MAGIC This demonstration builds on the **Canada Sales** dashboard you began in an earlier demo. Be sure that you have completed that demo, entitled *Creating Visualizations and Adding Summary Statistics*, before proceeding.
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
-- MAGIC These tables contain simulated business-to-business order and opportunity data for an imaginary company's Canadian sales operation. The **ca_orders** table contains information from 2021 through the middle of November 2024. This table identifies the relevant customer with a unique key that points into the **ca_customers** table, and it identifies the relevant product with a unique key that points into the **ca_products** table. The **ca_opportunities** table provides additional details regarding sales opportunities and sales representatives. You'll use the data in these tables to prepare your dashboard.
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
-- MAGIC To use the Databricks Catalog Explorer to see your newly loaded data, follow the steps below.
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
-- MAGIC ### A: Experiment with Cross-filtering
-- MAGIC
-- MAGIC The visualization widgets in Databricks dashboards offer interactivity by default. Let's see this capability in action.
-- MAGIC
-- MAGIC **📌 NOTE:** Many of the following instructions take place in a non-notebook area of the platform. It is recommended to open either the notebooks in a separate tab or window to reference the instructions alongside the area where they are performed.
-- MAGIC
-- MAGIC 1. Select **Dashboards** from the sidebar navigation. (It is recommended to right-click and select Open Link in New Window or Tab)
-- MAGIC
-- MAGIC 1. Click on the **Canada Sales** dashboard you began building in an earlier activity.
-- MAGIC 1. Navigate to the **Overview** page tab.
-- MAGIC 1. Click on one of the segments of the pie chart. What happens to the rest of the display? Do all of the visualizations react, or just some of them?
-- MAGIC 1. Click again on the same segment of the pie chart to restore the display to what it was previously.
-- MAGIC 1. Experiment with clicking on other graphical components to see the reactions. Don't forget to undo your actions by clicking again. How can you tell that cross-filtering is in action? 
-- MAGIC
-- MAGIC Cross-filtering applies to all the visualizations on a given page of a dashboard that are based on the same dataset.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B: Implement a Local Filter Widget
-- MAGIC
-- MAGIC Filter widgets affect all visualizations on the same page that are based on the same dataset. They offer finer grained control that does cross-filtering, and they also make your dashboard more self-describing. Anyone who sees the filter widget's current settings will assume that the other dashboard components they see are being filtered. 
-- MAGIC
-- MAGIC 1. If you moved away, select **Dashboards** from the sidebar navigation.
-- MAGIC 1. Click on the **Canada Sales** dashboard you began building in an earlier activity.
-- MAGIC 1. Navigate to the **Overview** page tab.
-- MAGIC 1. Click the icon in the palette for adding a filter, which looks like a tiny funnel.
-- MAGIC 1. Land the new widget wherever it is convenient. Click in the new widget to give it focus.
-- MAGIC 1. When the filter widget is selected, the filter configuration panel appears on the right side of the screen.
-- MAGIC
-- MAGIC 1. Apply the following settings:  
-- MAGIC   - **Filter**: Date range picker
-- MAGIC   - **Fields**: Expand the **Orders22** dataset and choose **orderdate**
-- MAGIC 8. Use the checkboxes to turn on **Title**.  
-- MAGIC
-- MAGIC 1. Click the placeholder title on the new filter widget and change it to **Order Date**  
-- MAGIC 1. Experiment with your filter widget. Which visualizations change when you define a date range? Do the tables on the other page change?

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C: Implement a Global Filter
-- MAGIC
-- MAGIC Global filters affect all visualizations throughout the dashboard that are based on the same dataset. They offer more global control of filtering. 
-- MAGIC
-- MAGIC 1. If you moved away, select **Dashboards** from the sidebar navigation.
-- MAGIC
-- MAGIC 1. Click on the **Canada Sales** dashboard you began building in an earlier activity.
-- MAGIC 1. Between the **Data** tab and the **Overview** tab, locate the Filter icon, which looks like a tiny funnel, and click it. This opens the **Global filters** side panel.
-- MAGIC 1. Click the **+** icon at the upper right of the side panel. 
-- MAGIC 1. In the Widget configuration panel, set the following:
-- MAGIC   - **Title:** Province Filter
-- MAGIC   - **Filter:** Single Value
-- MAGIC   - **Fields:** 
-- MAGIC     - Table: Orders22
-- MAGIC     - Field: province
-- MAGIC
-- MAGIC 6. Experiment with your filter widget. Which visualizations change when you define a date range? Do the tables on the other page change?
-- MAGIC
-- MAGIC 1. Navigate to the **Source Data** page of the Dashboard. Did this filter also impact what was visible there?

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
