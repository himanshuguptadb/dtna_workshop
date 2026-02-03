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
-- MAGIC ## 1.08 Demo - Sharing Dashboards with Stakeholders and Others
-- MAGIC
-- MAGIC Databricks AI/BI Dashboards help you quickly transform data into shareable insights. 
-- MAGIC
-- MAGIC In this lesson, we’ll learn about how to share your dashboards with your colleagues, especially those who will depend on them for business intelligence.
-- MAGIC
-- MAGIC This demonstration builds on the **Canada Sales** dashboard you have been working with in earlier demos. Be sure that you have completed the previous demo, entitled *Filters and Parameters*, before proceeding.
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
-- MAGIC You can also enrich your organization's web pages, typically intranet pages, by embedding a window in which website visitors can interact with a dashboard.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### A: Browse for existing dashboards
-- MAGIC
-- MAGIC Before sharing a dashboard, it is wise to see what other dashboards already exist. Does your new dashboard duplicate an existing one? Are there design conventions or naming conventions for dashboards that you should follow? Let's examine what else might be already published.
-- MAGIC
-- MAGIC **📌 NOTE:** Many of the following instructions take place in a non-notebook area of the platform. It is recommended to open either the notebooks in a separate tab or window to reference the instructions alongside the area where they are performed.
-- MAGIC
-- MAGIC 1. Select **Dashboards** from the sidebar navigation. (It is recommended to right-click and select Open Link in New Window or Tab)
-- MAGIC 1. The resulting screen lists all the dashboards which we have at least permission to view. In this classroom environment, what we see here is determined by our lab configuration. In your organization's actual Databricks workspace, you will see a variety of dashboards here.
-- MAGIC 1. At the top of the screen, there is a search box labeled "Search data, notebooks, recents, and more". Click in this box and type **canada sales**. What types of items were found?

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B: Publish the dashboards and define permissions
-- MAGIC
-- MAGIC While permissions on your data are managed by Unity Catalog, permissions on AI/BI Dashboards are managed at the level of the SQL workspace. In Databricks, a workspace is a Databricks deployment in the cloud that functions as an environment for your team to access Databricks assets. This means that you must think about two different kinds of permission issues:
-- MAGIC
-- MAGIC - What Unity Catalog credentials will users use to access the dashboard's underlying data? And
-- MAGIC - What rights does each user have to the dashboard itself?
-- MAGIC
-- MAGIC This may seem complex, but in practice there are a few common patterns, and we'll see the most common one in this lab.
-- MAGIC
-- MAGIC When your dashboard is complete, you can publish it and share it with others. 
-- MAGIC
-- MAGIC Published dashboards can be shared with other users in your workspace and with users registered at the account level. That means that users registered to your Databricks account, even if they have not been assigned workspace access or compute resources, can be given access to your dashboards.
-- MAGIC
-- MAGIC When you publish a dashboard, the default setting is **Share data permission**. Share data permission in your published dashboard allows dashboard viewers to use your data permissions to access the data and power the queries that support it. This enables a shared cache, which can improve performance. If you choose **Individual data permission**, each viewer of the published dashboard uses their own data permissions to run queries. This can lead to more frequent refresh operations. If a viewer does not have access to the underlying data or the default SQL warehouse that powers the dashboard, _visualizations will not render._  
-- MAGIC
-- MAGIC You can also notify viewers by sending emails to individuals or small groups when the dashboard is published.
-- MAGIC
-- MAGIC #### Publishing a Dashboard
-- MAGIC
-- MAGIC To publish your dashboard, complete the following steps:
-- MAGIC
-- MAGIC 1. Select **Dashboards** from the sidebar navigation.
-- MAGIC
-- MAGIC 1. In the dashboard selector, locate and click on the dashboard titled **Canada Sales** that is owned by you.
-- MAGIC 1. Click **Publish** in the upper-right corner of your dashboard. Read the setting and notes in the **Publish** dialog.
-- MAGIC 1. In the **Publish** dialog, you’ll see two data permission options. Make sure to select **Share data permission**.
-- MAGIC 1. Optionally, you can notify viewers via email and describe your changes in the text field.
-- MAGIC 1. Click **Publish** in the lower-right corner of the dialog. The **Sharing** dialog should open afterward. If it does not open, you can select **Share** next to **Publish** at the top of the dashboard.
-- MAGIC     - You can use the text field to search for individual users, or share the dashboard with a preconfigured group, like **Admins** or **All workspace users**. From this window, you can grant leveled privileges like **Can Manage** or **Can Edit**. See <a href="https://docs.databricks.com/en/security/auth-authz/access-control/index.html" target="_blank">Dashboard ACLs</a> for details on permissions.
-- MAGIC     - The bottom of the **Sharing** dialog controls view access. Use this setting to easily share with all account users.
-- MAGIC 1.  Under **Sharing settings**, choose **Anyone in my account can view** from the drop-down. Then, close the **Sharing** dialog.
-- MAGIC 1. Use the context icon at the top of the dashboard next to the dashboard name to switch between **Edit Draft** and **View Published** versions of your dashboard. 
-- MAGIC
-- MAGIC **📌 Note:** When you edit your draft dashboard, viewers of the published dashboards do not see your changes until you republish. The published dashboard includes visualizations that are built on queries that can be refreshed as new data arrives. When dashboards are refreshed, they are updated with new data automatically; the dashboards do not need to be republished.
-- MAGIC
-- MAGIC ---
-- MAGIC *But what about security?*
-- MAGIC
-- MAGIC When you published your dashboard just now, you embedded your Unity Catalog credentials with the dashboard, and you allowed anyone on your organization to view the dashboard. This is suitable for comparatively less sensitive dashboards. For more sensitive information, where only a few named members of your organization should have access rather than everyone, the opposite pattern is common: 
-- MAGIC - *Not* embedding your credentials with the dashboard, so that dashboard viewers' own Unity Catalog credentials are checked; and
-- MAGIC - Granting **Can View** access only to named individuals in your Databricks account.
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### C: Embedding a dashboard in a web page
-- MAGIC
-- MAGIC Some information we want to share broadly within our organization. Perhaps I work on a team where everyone regularly consults an intranet server to learn about how the company is doing. If we have an AI/BI dashboard that tracks our progress towards some shared goal, it would be extremely motivating to embed the dashboard directly in the intranet home page. 
-- MAGIC
-- MAGIC This is simplest to deploy for information of comparatively low sensitivity, because your intranet server does not have the technical capability to check Unity Catalog rights or SQL workspace permissions. If users who lack either permission navigate to the intranet page we created, they will see an error message instead of the dashboard.
-- MAGIC
-- MAGIC 1. Select **Dashboards** from the sidebar navigation.
-- MAGIC
-- MAGIC 1. In the dashboard selector, locate and click on the dashboard titled **Canada Sales**.
-- MAGIC 1. Click on the **Share** button at top right.
-- MAGIC 1. In the resulting **Sharing** window, the option to **<> Embed dashboard** will be in the lower left.
-- MAGIC
-- MAGIC Due to the restrictions necessary to secure the demonstration and lab environments, you will be unable to go any further as embedding dashboards is disabled from these workspaces. However, if you are in your own environment with appropriate permissions, after selecting the option to **<> Embed dashboard**, you will see a new window entitled **Copy embed code**. This window contains HTML code that embeds this dashboard in a web page. 
-- MAGIC
-- MAGIC ![Embedded Dashboard iframe HTML code example](../Includes/images/embed_dashboard_example.png)
-- MAGIC
-- MAGIC In your actual Databricks deployment, you would work with your intranet team to paste this HTML into a web page and make it available through your web server.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
