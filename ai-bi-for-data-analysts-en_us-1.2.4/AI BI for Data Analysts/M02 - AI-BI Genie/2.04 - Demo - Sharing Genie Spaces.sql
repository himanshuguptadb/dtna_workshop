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
-- MAGIC ## 2.04 Demo - Sharing Genie Spaces
-- MAGIC
-- MAGIC Databricks AI/BI Genie empowers your end users by allowing them to have natural language chats directly with your organization's data. 
-- MAGIC
-- MAGIC In this activity you’ll learn how to share Genie spaces with end-users who will use them for self-service analytics. You’ll also learn how to ensure stakeholders and non-technical users understand how to provide feedback on Genie Spaces' responses and information. 
-- MAGIC
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
-- MAGIC ### A: Managing Genie space users' permissions
-- MAGIC
-- MAGIC As a practical matter, you will probably have two main groups of other Databricks users you care about:
-- MAGIC - Your audience of end users, who should be able to interact with your Genie space and get value from it but not reconfigure it, and
-- MAGIC - Your collaborators, who should be able to act on audience feedback to improve the Genie space for its users.
-- MAGIC
-- MAGIC You can control the rights that other people have on your Genie space through the **Sharing** dialogue.
-- MAGIC
-- MAGIC **📌 NOTE:** Many of the following instructions take place in a non-notebook area of the platform. It is recommended to open either the notebooks in a separate tab or window to reference the instructions alongside the area where they are performed.
-- MAGIC
-- MAGIC 1. If you are not already looking at the **Canada Sales and Opportunities Current Year** Genie space, navigate to it through **Genie** in the sidebar navigation. (It is recommended to right-click and select Open Link in New Window or Tab)
-- MAGIC
-- MAGIC 1. Click **Share** at top right.
-- MAGIC 1. Notice that at top there is a search box where you can search for already-defined users and groups. Can you enter an arbitrary email address in this box?
-- MAGIC 1. Depending on your classroom's configuration, you may be able to search for other learners by name in this search box. (In your organization's Databricks estate, your coworkers will appear here.) If you find other names, select one, and then take a note of the pulldown at right that allows you to define their permission levels.
-- MAGIC 1. You may also be able to share to groups. Groups of users are typically defined and maintained by your organization's platform administrators. Where possible, assigning permissions to role-based groups is always preferable to assigning permissions to named individuals, because it means there is less maintenance work required on your part and greater security for your organization's data.
-- MAGIC 1. There are two workspace-level system groups in each workspace: users and admins. Type `Admins` into the search box and assign this group **Can Edit** permissions. Turn off, for now, the checkbox underneath the newly added group name that says **Email new users**. Then click **Add**. The change takes effect immediately.
-- MAGIC 1. Type `All workspace users` into the search box and assign this group **Can View** permissions. Then click **Add**. The change takes effect immediately.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### B: Communicating about a new Genie space
-- MAGIC
-- MAGIC When you invite new users to a Genie space, it is very important that expectations are set. What are you asking them to do with the Genie space? Unless you tell them, they may not know what business purpose you expect them to put the Genie space to. Titling the Genie space descriptively and defining meaningful sample questions helps a lot. 
-- MAGIC
-- MAGIC If you add a new user while the **Email new users** checkbox is checked, newly added users will receive a system-generated email containing a link to the Genie space. Many Genie users prefer instead to share Genie spaces together with business context in a custom email that comes from them rather than from their organization's Databricks estate.
-- MAGIC
-- MAGIC 1. If you closed it, click the **Share** button to re-open the sharing window.
-- MAGIC 1. Click on the **Copy link** icon at lower left, which will copy the URL of the deployed Genie space to your clipboard. 
-- MAGIC 1. Create an incognito window in your browser.
-- MAGIC 1. Open the copied URL in this window.
-- MAGIC
-- MAGIC Notice that Databricks prompts for a user login. Only known users have access to Genie spaces.
-- MAGIC
-- MAGIC In your organization's actual Databricks deployment, you would probably instead paste this URL into a custom email to the Genie space's intended users. It's recommended that you clarify the following points in your communication regarding the Genie space when you share it's link:
-- MAGIC
-- MAGIC - The business purpose of the Genie space
-- MAGIC - What you expect the recipients to do with the Genie space
-- MAGIC - What level of access they have to the space (particularly edit or run)
-- MAGIC - A reminder that AI is imperfect, and that they should check Genie's responses by inspecting data
-- MAGIC - A reminder that Genie spaces rely on user feedback to be successful, so they should give thumbs-up and thumbs-down feedback to Genie's responses
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
