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
# MAGIC # Lab: Building Information Extraction Agents with Agent Bricks
# MAGIC _Tech Summit 2025_
# MAGIC
# MAGIC In this lab, you will build a workflow that will do the following: 
# MAGIC 1. Use Agent Bricks for parsing PDFs and initiate a Job
# MAGIC 1. Build on top of the automatically created Job to start an AI engineering pipeline to scale to process multiple PDFs
# MAGIC 1. Use Agent Bricks again as a downstream component of the pipeline that will extract information from parsed PDFs
# MAGIC 1. View the trace of the Information Extraction Agent with MLflow 
# MAGIC
# MAGIC This lab is meant to be a starting point for building out your own POC with Agent Bricks and does not cover all use cases. 
# MAGIC
# MAGIC ### Learning Objectives:
# MAGIC By the end of the lab, you will be able to: 
# MAGIC - Understand how to use the Agent Bricks UI to parse PDFs and create an Information Extraction Agent. 
# MAGIC - Understand how the SQL function `ai_parse_document()` is used for parsing PDFs.
# MAGIC - Understand how `ai_query()` can be leveraged to use your Information Extraction Agent endpoint. 
# MAGIC - Build on top of an automatically-generated Job for enhanced AI engineering tasks. 
# MAGIC - Demonstrate how to flatten a VARIANT type, which is necessary when using the Parse PDFs feature with Agent Bricks.
# MAGIC - Understand how MLflow's tracing feature is automatically leveraged with Agent Bricks.  
# MAGIC
# MAGIC #### Scenario
# MAGIC You are ingesting PDFs from cloud storage and you are leveraging Lakeflow Connect to land them in a volume called `build-agent-vol`. You now want to use generative AI to help extract information from these documents. Here is a diagram to help visualize the workflow you will implement. We will assume PDFs have already landed in your volume. 
# MAGIC
# MAGIC ![Agent Bricks Overview](Includes/Images/workflow-image.png)
# MAGIC
# MAGIC _It's important to keep in mind that Agent Bricks is intended to be a no-code solution for building Agents on Databricks_

# COMMAND ----------

# MAGIC %md
# MAGIC ## REQUIRED - SERVERLESS COMPUTE
# MAGIC
# MAGIC Before executing cells in this notebook, please be aware that **Serverless** is enabled by default.
# MAGIC
# MAGIC Follow these steps to select the classic compute cluster:
# MAGIC
# MAGIC 1. Navigate to the top-right of this notebook and click the drop-down menu to select your cluster. By default, the notebook will use **Serverless**.
# MAGIC
# MAGIC 1. Select **Serverless** or run the lab setup cell (the first cell down below). Either way, this notebook will connect to **Serverless**. 
# MAGIC
# MAGIC 1. If another cluster is available, do not select it and continue to the next cell.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC Run the following cell to configure your working environment for this notebook. This will take about 1 minute to complete.
# MAGIC
# MAGIC **NOTE:** The `DA` object is only used in Databricks Academy courses and is not available outside of these courses. It will dynamically reference the information needed to run the course in your lab environment.

# COMMAND ----------

# MAGIC %run ./Includes/Lab-Setup-01a

# COMMAND ----------

# MAGIC %md
# MAGIC Run the cell below and note that your default catalog and schema have been set to **dbacademy** and your **labuser** schema by the classroom setup script, in order to avoid using the three-level namespace.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT current_catalog(), current_schema();

# COMMAND ----------

# MAGIC %md
# MAGIC ## What is Agent Bricks? 
# MAGIC Agent Bricks provides a simple, no-code approach to build and optimize domain-specific, high-quality AI agent systems for common AI use cases. It streamlines the implementation of AI agent systems so that users can focus on the problem, data, and metrics instead.
# MAGIC
# MAGIC Agent Bricks is powered by Databricks Mosaic AI to allow users to deploy comprehensive AI agent systems customized with their unique data quickly and easily.
# MAGIC
# MAGIC - Specify your problem by specifying your use case and point to your data.
# MAGIC - Agent Bricks automatically builds out the entire AI agent system for you. Agent Bricks will automatically try various AI models, fine-tune them using your data, optimize the systems using innovative AI techniques, and evaluate them to offer you the best built-out systems.
# MAGIC - Further refine the system for continuous improvement. When you use Agent Bricks, Databricks will run additional methods and hyperparameter sweeps in the background to continually optimize your model result. If our evaluations indicate a different model would achieve better results, Databricks will notify you without additional charge.
# MAGIC
# MAGIC Additionally, Agent Bricks is seamlessly integrated with the rest of the Databricks Data Intelligence Platform. This means you have everything you need to deploy AI solutions, from security and governance to data integration, vector indexes, and quality evaluation. This is all available as a one-button optimized deployment.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Using Agent Bricks for Parsing PDFs
# MAGIC In this first step, we will using Agent Bricks for parsing a single PDF. Later, we will scale this to more than one PDF via a pipeline we will build with Jobs. 
# MAGIC
# MAGIC ### Instructions
# MAGIC - Explore the data
# MAGIC   - Navigate to **Catalog** and inspect the volume called `build_agents_vol`. This contains two directories called **_single_pdf** and **_multiple_pdfs**.
# MAGIC   - [Here is an example of one of the PDFs](https://arxiv.org/abs/2203.02155). 
# MAGIC - Parse the PDF in **_single_pdf**
# MAGIC   1. Navigate to **Compute** and make sure the SQL warehouse called `agent_XS` is running. Each user will have their own SQL warehouse as a part of the environment setup for this lab in Vocareum.
# MAGIC   1. Navigate to **Agents** on the left side menu. Note that you will see a tag next to **Agents** that says this feature is still in **Beta**. 
# MAGIC   1. On the **Information Extraction** tile, click on **Use PDFs**.
# MAGIC   1. Under **Select folder with PDFs or images**, select the _folder_ `_single_pdf` in `build_agents_vol`. It's important to realize that you are selecting the _directory_ and not the _file_ to upload. Click confirm.
# MAGIC   1. For **Choose the schema for the destination table**, select the same schema that contains the volume your explored earlier. This will be of the form **labuserXXX**. 
# MAGIC   1. For the **Destination table name**, add `01` in front of the default name. That is, the full name will read `01_single_pdf_parsed`. 
# MAGIC     > We will use a numbering system with tables to indicate the step within our overall workflow for this lab.  
# MAGIC   1. Click **Start import**. 
# MAGIC
# MAGIC - In the side menu, you will see a job with the status **Running**. Click on it. This will take you to a task that has been automatically created. The Job that was created has the default job name **parse_pdfs_to_delta**. This job has a single _task_ with the following configurations: 
# MAGIC   1. _Task name_: parse_pdfs_to_delta (same as the job name)
# MAGIC   1. _Type_: SQL
# MAGIC   1. _SQL_: Query
# MAGIC   1. _SQL query_: parse_pdfs_to_delta
# MAGIC   1. _SQL warehouse_: agent_XS (XS)
# MAGIC   
# MAGIC   Additionally, there are default parameters that have been assigned to the task for the SQL query as part of the job creation. Of these parameters, only **limit** (required) will be defined if you inspect the job. The other parameters were passed to the sql query when the job ran using the Agent Bricks UI and therefore will be left blank (not required).
# MAGIC   1. _Parameters_: 
# MAGIC       - destinationTableName: **dbacademy.labuserXXX.01_single_pdf_parsed**
# MAGIC       - sourceVolumePath: **/Volumes/dbacademy/labuserXXX/build_agents_vol/_single_pdf**
# MAGIC       - limit: **100**
# MAGIC     > Later, we can and will overwrite these values. 
# MAGIC
# MAGIC - This SQL query chains multiple CTEs to ingest a batch of files; conditionally AI-parse or raw-decode them; split parsed documents into pages and reassemble the content; combine both parsed and raw results; and finally materialize the output into a new table for downstream analysis.
# MAGIC   > You can always view/edit the SQL query by navigating to **Queries** under **SQL**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Building a Workflow 
# MAGIC Next, take the generated SQL code and build out a workflow. 
# MAGIC
# MAGIC ### Instructions
# MAGIC - As a part of the classroom setup, there is a notebook called **Lab 01b - Flattening Parsed PDFs**. Navigate to complete the instructions there. Proceed with the next set of instructions only after completing the notebook **Lab 01b - Flattening Parsed PDFs**.
# MAGIC
# MAGIC - Select **Jobs & Pipelines** from the sidebar navigation, and navigate back to the job named `parse_pdfs_to_delta`.
# MAGIC
# MAGIC - Now, select the **Tasks** tab, click on **+ Add task**, and choose the **Notebook** type.
# MAGIC      - Name the new task `flatten_parsed_pdfs`.
# MAGIC      - Set the **Path** to the notebook you completed in the previous task (**Lab 01b – Flattening Parsed PDFs**)
# MAGIC      -  For compute, you may leave it as serverless, but make sure you select **Performance optimized** on the right. Otherwise, your job will take a few minutes to run (like classic compute). This option will only be available after you've create a new task since it requires certain workloads. 
# MAGIC      - Update the parameterization of the notebook to account for `target_table_name` and `source_table_name`. Use the Jobs UI to set the values for these keys as `02_pdf_parsed_flattened` and  `01_single_pdf_parsed`, respectively. 
# MAGIC      - Now, Click **Create Task**.
# MAGIC
# MAGIC - Before running the job, we need to update our SQL Query from Part 1. The reason is because our table already exists and the current query will try to create the table from scratch. Navigate to the SQL query (**parse_pdfs_to_delta**) via the **Queries** option in the sidebar navigation, and update the third line to:  
# MAGIC   `CREATE TABLE IF NOT EXISTS IDENTIFIER(:destinationTableName) AS (`
# MAGIC
# MAGIC **Note:** Make sure you are attached to the `XS Serverless` compute and **Save** the query.
# MAGIC
# MAGIC - Lastly, we need to input SQL Query values at the Job level (we noted this in the previous section). Input the parameters shown here from before (be sure to update it with your labuser name):
# MAGIC
# MAGIC   - _Parameters_: 
# MAGIC     - destinationTableName: **dbacademy.labuserXXX.01_single_pdf_parsed**
# MAGIC     - sourceVolumePath: **/Volumes/dbacademy/labuserXXX/build_agents_vol/_single_pdf**
# MAGIC     - limit: **100**
# MAGIC
# MAGIC - After filling out all the required parameters, click the **Apply changes** button and **Save** the query.
# MAGIC
# MAGIC - Navigate back to the `parse_pdfs_to_delta` job and **Run** the job 
# MAGIC - Go to the **Runs** tab to view active and completed executions of the job.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Ready to Scale
# MAGIC If the job was successful, you are now ready to scale the input to multiple PDFs. Again, this provided as a part of the setup for this lab in the directory `_multiple_pdfs`. 
# MAGIC
# MAGIC ### Instructions
# MAGIC - Select the **Tasks** tab and navigate to the task `parse_pdfs_to_delta`. 
# MAGIC   > **Note:** Throughout these instruction, replace `labuserXXX` with your actual username.
# MAGIC   - Change the parameter value for `destinationTableName` to `dbacademy.labuserXXX.03_multiple_pdf_parsed`.
# MAGIC   - Change the parameter value for`sourceVolumePath` to `/Volumes/dbacademy/labuserXXX/build_agents_vol/_multiple_pdfs`.
# MAGIC   - Save your task.
# MAGIC
# MAGIC - Navigate to the task `flatten_parsed_pdfs`, and update the parameter values
# MAGIC   - Change the target table to `04_multiple_pdf_parsed_flattened`.
# MAGIC   - Change the source table to `03_multiple_pdf_parsed`. 
# MAGIC   - Save your task.
# MAGIC
# MAGIC - Run the workflow again to parse and flatten the PDFs into a Delta table.
# MAGIC > Because we took care to parameterize the notebook, making the update to target and source tables won't cause any issues. 
# MAGIC - If the Job was successful, then you are ready for the next part of the lab, which will use an Information Extraction Agent to extract information from our table `04_multiple_pdf_parsed_flattened`.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Information Extraction with Agent Bricks
# MAGIC In this step, you will use the resulting table `04_multiple_pdf_parsed_flattened` to extract some information from the parsed PDFs from the previous step. In fact, you will rely on how the AI function `ai_parse_document()` parsed your PDFs to extract valuable information from each chunk that was returned in our Delta table `04_multiple_pdf_parsed_flattened`.
# MAGIC > For further reading on `ai_parse_document()`, see [this documentation](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_parse_document). 
# MAGIC
# MAGIC ### Instructions
# MAGIC - Navigate to **Agents** from the sidebar navigation.
# MAGIC - Select **Build** in the **Information Extraction** tile. 
# MAGIC - In the **Browse text data** box, type (or copy and paste) `04_multiple_pdf_parsed_flattened` and press **Use this table**. 
# MAGIC - Select the column labeled `content` as the column to extract information from. 
# MAGIC - Next, we need to provide a sample output. The agent will use it to _infer_ the schema, which can be edited. As a part of the lab configuration, you have been provided with a `.json` file located in the subdirectory where this notebook is located: 
# MAGIC   - Click on `json_samples` → `information_extraction_example.json`. 
# MAGIC   - Open it and copy and paste its contents into the **Sample output** text field.
# MAGIC     > This particular Agent will be used to extract the citation, authors being cited, year of publication, description of methodology, and relevance.  
# MAGIC - Give the agent the name **labuserXXX-agent**, where you should replace **labuserXXX** with your username.
# MAGIC - Click **Create agent**. 
# MAGIC - This will take you to the build tab. Review the results and click **Use your agent** in the bottom right. 
# MAGIC - On the next screen, you can click **Start extraction** to begin extracting this information from all the documents processed. This will automatically build a SQL statement that uses `ai_query()` to query this Agent's endpoint. Attach the SQL notebook to your SQL Warehouse (agent_XS) and click **Run** to generate results. 
# MAGIC > Note that only the first 20 rows will be queried by default.
# MAGIC - Notice that in the **response** column, we see a lot of `null` values in the set of parsed chunks. This means our agent wasn't able find the information we requested. Explore some of the outputs in **response** before moving on to the final section.

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Updating our Agent's Configuration Response
# MAGIC Let's end this demo by adding an additional field to our instructions for the agent.  
# MAGIC ### Instructions
# MAGIC - Navigate back to the Information Extraction Agent you created in the previous step. 
# MAGIC - Click on **Add new field** of Agent configuration in the **Build** tab. 
# MAGIC - Enter `summary` as the field name. 
# MAGIC - Make this a **required** field. 
# MAGIC - Set the **type** to **String**. 
# MAGIC - For the description, copy and paste the following prompt: _A string that summarizes the content. _. 
# MAGIC - Click **Confirm** and click **Update agent** on the bottom right. 
# MAGIC - Use the agent again to see the additional output that includes a summary. 
# MAGIC   > How can you make this **Summary** field better?

# COMMAND ----------

# MAGIC %md
# MAGIC ## F. MLflow Trace Inspection
# MAGIC Your final task is to navigate to **Experiments** using the menu on the left side of the screen and select the agent endpoint. Here you can view the Trace using the UI. MLflow Tracing is a powerful feature that provides end-to-end observability for gen AI applications, including complex agent-based systems. It records inputs, outputs, intermediate steps, and metadata to give you a complete picture of how your app behaves. You can view the request and response from using the agent endpoint.

# COMMAND ----------

# MAGIC %md
# MAGIC ## G. Further Agent Capabilities and Information
# MAGIC Because Agent Bricks is built on Databricks, you can use it across the platform. There are additional capabilities that will be out of scope for this lab, but are worth mentioning. Navigate back to the agent and go to the **Use** tab once more. There are two additional capabilities (that are in Beta) that you can read more about down below: _Create DLT pipeline_ and _Get a cheaper agent_.
# MAGIC
# MAGIC #### Lakeflow Declarative Pipelines
# MAGIC Selecting **Create DLT pipeline** will automatically generate declarative source code for building a streaming table that queries the entire table `04_multiple_pdf_parsed_flattened`. 
# MAGIC
# MAGIC > [Lakeflow Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/dlt/) is a framework for creating batch and streaming data pipelines in SQL and Python. Common use cases for Lakeflow Declarative Pipelines include data ingestion from sources such as cloud storage (such as Amazon S3, Azure ADLS Gen2, and Google Cloud Storage) and message buses (such as Apache Kafka, Amazon Kinesis, Google Pub/Sub, Azure EventHub, and Apache Pulsar), and incremental batch and streaming transformations.
# MAGIC
# MAGIC #### Agent Optimization
# MAGIC
# MAGIC If you want to optimize your agent, you need at least 100 inputs (either 100 rows in a Unity Catalog table or 100 manually-provided examples). This step is omitted in this lab because optimization can take about an hour. Making changes to your currently active agent is blocked when optimization is in progress. [Metrics are logged to your MLflow run per-field](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/key-info-extraction) (aggregated to the top-level field) when using an optimized agent. You can read more [here](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/custom-llm#step-3-try-out-and-optimize-your-agent). 
# MAGIC
# MAGIC #### Agent Bricks Blog Post
# MAGIC See [our blog](https://www.databricks.com/blog/introducing-agent-bricks) post about Agent Bricks for additional reading and customer successes. 
# MAGIC
# MAGIC #### Relevant Additional Courses
# MAGIC - [Data Ingestion with Lakeflow Connect](https://www.databricks.com/training/catalog?search=data+ingestion)
# MAGIC - [Generative AI Course](https://www.databricks.com/training/catalog?search=generative+ai)

# COMMAND ----------

# MAGIC %md
# MAGIC ## H. Cleaning up your agent
# MAGIC Once you are finished with testing your Information Extraction Agent, complete the following tasks to successfully delete it:
# MAGIC 1. Click on **Agents** in the left side menu.
# MAGIC 1. Hover over the three vertical dots next to the agent you want to delete and click on them. 
# MAGIC 1. Select **Delete**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## I. Challenge Questions
# MAGIC
# MAGIC 1. How would you update **Lab 01b - Flattening Parsed PDFs** to avoid rewriting the table each time? This will move your POC from a complete overwrite to updating only when new PDFs land in your volume.
# MAGIC 1. How would you update your Job so you only process files when they land in the volume? This would allow for automatic pipeline runs to process your PDFs.
# MAGIC 1. Architect a workflow to include the Lakeflow Declarative Pipeline option. What are the limitations?

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
