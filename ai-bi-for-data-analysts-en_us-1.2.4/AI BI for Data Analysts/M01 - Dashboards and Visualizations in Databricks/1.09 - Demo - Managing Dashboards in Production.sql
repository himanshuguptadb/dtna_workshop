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
-- MAGIC ## 1.09 Demo - Managing Dashboards in Production
-- MAGIC
-- MAGIC Databricks AI/BI Dashboards help you quickly transform data into shareable insights. 
-- MAGIC
-- MAGIC In this lesson, we’ll learn how to manage and update dashboards, including how and when changes made in draft impact the version of the dashboard visible to others. We’ll also discuss some of the established best practices regarding when to update, refresh, and adjust datasets and additional dashboard settings. 
-- MAGIC
-- MAGIC This demonstration builds on the **Canada Sales** dashboard you have been working with in earlier demos. Be sure that you have completed the previous demo, entitled *Sharing Dashboards with Stakeholders and Others*, before proceeding.
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
-- MAGIC ### A: Learn about dashboard refreshes
-- MAGIC
-- MAGIC Now that we have a published dashboard, let's try modifying the data it's based on. Will the dashboard automatically change?
-- MAGIC
-- MAGIC **📌 NOTE:** Throughout these instructions, replace `YOURSCHEMA` with the name of your schema. (You can find your schema name in the setup run cell that you have just executed.) Additionally, many of the following instructions take place in a non-notebook area of the platform. It is recommended to open either the notebooks in a separate tab or window to reference the instructions alongside the area where they are performed.
-- MAGIC
-- MAGIC 1. Select **Dashboards** from the sidebar navigation. (It is recommended to right-click and select Open Link in New Window or Tab)
-- MAGIC 1. In the dashboard selector, locate and click on the dashboard titled **Canada Sales**. 
-- MAGIC
-- MAGIC 1. Edit the following SQL cell, replacing both occurrences of `YOURSCHEMA` with the name of your personal schema. Then run the cell by clicking the "Run" triangle in its upper left corner. This block of SQL changes all of Ingrid's recorded sales amounts in the **ca_orders** table to one cent. It then prints out a few of Ingrid's orders so that we can confirm our change.

-- COMMAND ----------

UPDATE dbacademy.YOURSCHEMA.ca_orders 
  SET orderamt = 0.01 WHERE salesrep = 'Ingrid' ;

SELECT salesrep, orderamt FROM dbacademy.YOURSCHEMA.ca_orders
  WHERE salesrep = 'Ingrid' LIMIT 5;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 4. Did the dashboard automatically update to reflect Ingrid's greatly reduced revenue? Wait a minute or two to see whether it updates on its own. 
-- MAGIC 1. When you become impatient, make a note of the time since the dashboard was last updated, shown at top right next to the Databricks refresh icon.
-- MAGIC 1. Before we click the Databricks refresh icon, let's try our browser's refresh button. In the Google Chrome browser, this is the button with a circular arrow to the left of the URL bar. The screen redraws. Note the display of the time since the last refresh in the redrawn screen. Did refreshing the web page result in newer data?
-- MAGIC 1. Finally, click the Databricks dashboard Refresh button at the top right of the dashboard (identified by its circular-arrow icon). Did this result in fresher data? What happens to the time-since-last-update display?
-- MAGIC 1. Let's restore the original version of the data. Edit the following SQL cell, replacing `YOURSCHEMA` with the name of your personal schema. Then run it by clicking its "Run" triangle at top left:

-- COMMAND ----------

RESTORE TABLE dbacademy.YOURSCHEMA.ca_orders TO VERSION AS OF 0;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC What this demonstrates is that dashboards do not automatically refresh, but are instead controlled through manual and scheduled refresh schedules.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B: Define a refresh schedule 
-- MAGIC
-- MAGIC Setting users' expectations about how frequently new data arrives in a dashboard is very wise. After all, if the gold-layer table upon which a dashboard is based only receives new records once every day, it is not useful for users to refresh the dashboard any more frequently. Setting a refresh schedule and communicating about it has  benefits:
-- MAGIC - Users experience less frustration due to waiting for new data that seems never to arrive.
-- MAGIC - You, the data analyst who maintains the dashboard, benefit by fielding fewer ad-hoc questions about data freshness.
-- MAGIC
-- MAGIC 1. Select **Dashboards** from the sidebar navigation.
-- MAGIC
-- MAGIC 1. In the dashboard selector, locate and click on the dashboard titled **Canada Sales**.
-- MAGIC 1. Confirm that you are viewing the published version of the dashboard. If not, use the **Edit draft** versus **View Published** context button at the top left of the dashboard to move to the **Published** version. 
-- MAGIC 1. Click on the **Schedule** button at top right. If applicable, select **+ Schedule**.
-- MAGIC 1. The resulting window has two tabs. In the **Settings** tab, set the dashboard to refresh every day at 4:00 in the morning.
-- MAGIC 1. Notice the **Timezone** selection. This selector is especially important for people who work in organizations spread across several timezones. For this activity, you can leave it at its default setting, which corresponds to the default timezone configured by your SQL warehouse.
-- MAGIC 1. Click **Create**.
-- MAGIC
-- MAGIC Now let's communicate about the change. 
-- MAGIC
-- MAGIC 8. Return to the **Draft** dashboard. 
-- MAGIC 1. Edit the text box containing the title widget to include a line below the title stating the dashboard's refresh schedule. 
-- MAGIC 1. Republish the dashboard.
-- MAGIC 1. Confirm that the note you added is visible.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C: Use Subscriptions
-- MAGIC
-- MAGIC Many of your dashboard users simply want a regular report. We can save them time by arranging for them to receive a recurring email, every time the dashboard updates, containing a snapshot of the first page. This is called a subscription. Let's set one up for ourselves.
-- MAGIC
-- MAGIC 1. Select **Dashboards** from the sidebar navigation.
-- MAGIC
-- MAGIC 1. In the dashboard selector, locate and click on the dashboard titled **Canada Sales**.
-- MAGIC 1. Confirm that you are viewing the published version of the dashboard. If not, use the **Edit draft** versus **View Published** context button at the top left of the dashboard to move to the **Published** version. 
-- MAGIC 1. Click on the **Schedule (1)** button at top right. You will notice that there is a **Subscribe** button to the right of the schedule. Click it. You are now subscribed to get a notification when this refresh schedule is triggered.
-- MAGIC 1. Using the kebab menu icon to the right of the **Subscribe** button, select **Edit**. From here you can switch the view to the **Subscribers** tab and view all users who've subscribed to that particular refresh schedule.
-- MAGIC
-- MAGIC Now we, and any other users we add, will get a recurring email containing a snapshot of the dashboard's first page at the time of the refresh scheduled. This email will also contain a link back to the dashboard in Databricks, so that authorized users can interact with the dashboard to learn more. But how should users handle this email? Is it sensitive information? Would it be appropriate for them to forward this email to their coworkers? To people outside the organization? Can they print the dashboard image? The answers to all these questions are determined by your organization's security policy.
-- MAGIC
-- MAGIC Let's add an indication of the sensitivity of the information to the dashboard. This doesn't prevent people from mishandling the information, but it does make them aware of your organization's expectations.
-- MAGIC
-- MAGIC 6. Return to the **Draft** dashboard. 
-- MAGIC 1. Edit the text box containing the title widget to include a new line at the bottom, with words to this effect:
-- MAGIC <br/>
-- MAGIC
-- MAGIC     ```
-- MAGIC     Proprietary and confidential. Do not forward outside the organization.
-- MAGIC     ```
-- MAGIC
-- MAGIC 11. Republish the dashboard.
-- MAGIC 1. Confirm that the note you added is visible. 
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
