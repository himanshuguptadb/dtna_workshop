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
# MAGIC # Demo - Automatic Agentic Systems with Agent Bricks
# MAGIC _Tech Summit 2025_
# MAGIC
# MAGIC In this demonstration, we will discuss how to use the PDF parsing tool along with the Information Extraction Agent within Databricks.  We will also discuss how to flatten the resulting Delta table from the parsed PDF, which is an integral component of AI engineering workloads. 
# MAGIC
# MAGIC #### Learning Objectives
# MAGIC _By the end of this demonstration, you will be able to:_
# MAGIC 1. Explain what Agent Bricks is as well as the supported use cases. 
# MAGIC 1. Know how to access the three supported Databricks-managed agents using the UI.
# MAGIC 1. Know how to use the **Parse PDF** feature with **Agent Bricks**.
# MAGIC 1. Know how to create, use, and improve an **Information Extraction Agent**. 
# MAGIC
# MAGIC _It's important to keep in mind that Agent Bricks (currently in Beta) is intended to be a no-code solution for building Agents on Databricks_

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
# MAGIC ## Environment Setup
# MAGIC
# MAGIC This notebook relies on Environment version 2. We need to ensure that the **Environment version** is set to 2.
# MAGIC 1. Navigate to the environment icon to the right of your workspace and click on it. 
# MAGIC ![Environment-Icon](Includes/Images/environment-icon.png)
# MAGIC 1. Under **Environment version** click on the dropdown menu and select 2. 
# MAGIC 1. Click **Apply**. 
# MAGIC 1. On the pop-up screen that says **Confirm action**, click **Confirm**. 
# MAGIC > See [here](https://docs.databricks.com/aws/en/compute/serverless/dependencies) for more information on configuring a serverless environment.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC Run the following cell to configure your working environment for this notebook. This will take about 1 minute to complete.
# MAGIC
# MAGIC **NOTE:** The `DA` object is only used in Databricks Academy courses and is not available outside of these courses. It will dynamically reference the information needed to run the course in your lab environment.

# COMMAND ----------

# MAGIC %run ./Includes/Demo-Setup-01

# COMMAND ----------

# MAGIC %md
# MAGIC Run the cell below and note that your default catalog and schema have been set to **dbacademy** and your **labuser** schema by the classroom setup script, in order to avoid using the three-level namespace.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT current_catalog(), current_schema();

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Introducing Agent Bricks
# MAGIC
# MAGIC ### What is Agent Bricks?
# MAGIC
# MAGIC Agent Bricks is a no-code solution for building and optimizing domain-specific, high-quality AI agent systems for common use cases. It simplifies the process so users can focus on their problem, data, and metrics.
# MAGIC
# MAGIC Powered by Databricks Mosaic AI, Agent Bricks enables users to quickly deploy tailored AI agent systems using their own data.
# MAGIC
# MAGIC - Define your use case and connect your data.
# MAGIC - Agent Bricks automatically constructs the entire AI agent system, experimenting with different AI models, fine-tuning them on your data, optimizing with advanced techniques, and evaluating to deliver the best solution.
# MAGIC - Continuously improve your system. Databricks runs additional methods and hyperparameter sweeps in the background to optimize results. If a better model is found, you’ll be notified at no extra cost.
# MAGIC
# MAGIC Agent Bricks is fully integrated with the Databricks Data Intelligence Platform, providing everything needed for AI deployment—including security, governance, data integration, vector indexes, and quality evaluation—all accessible with a single optimized deployment.
# MAGIC
# MAGIC ##### Current Supported Use Cases
# MAGIC Currently, the supported use cases include **Information Extraction**, **Model Specialization**, **Knowledge Assistant**, and **Multi-Agent Supervisor**. You can read more [here](https://docs.databricks.com/aws/en/generative-ai/agent-bricks#supported-use-cases). 
# MAGIC
# MAGIC ##### General Workspace Requirements 
# MAGIC For workspace requirements to try Databricks out in your own workspace, please see [this documentation](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/#requirements).
# MAGIC
# MAGIC ##### What about Customer Privacy? 
# MAGIC Agent Bricks is a [Databricks Designated Service](https://docs.databricks.com/aws/en/resources/designated-services), which means that it uses [Databricks Geos](https://docs.databricks.com/aws/en/resources/databricks-geos) to manage data residency when processing customer content.

# COMMAND ----------

# MAGIC %md
# MAGIC ### A1. Enabling and Opening Agent Bricks
# MAGIC
# MAGIC Once [enabled](https://docs.databricks.com/aws/en/admin/workspace-settings/manage-previews), you can access Databricks managed agents in the left side menu (see image). As a part of the Vocareum lab setup, this has been automatically enabled for you. Navigate to the left side menu and click on **Agents**. 
# MAGIC
# MAGIC <img src="Includes/Images/agent-button.png" alt="Agent Bricks Overview" width="200"/>
# MAGIC
# MAGIC > Note that Agent Bricks is still currently in [beta](https://docs.databricks.com/aws/en/release-notes/release-types). For a list of other beta features offered by Databricks, please see our early-stage products list [here](https://www.databricks.com/product/pricing/beta-products). _This workspace has been specially configured for this demo and lab, so it will not contain all beta features._

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Parsing PDFs
# MAGIC As a part of the classroom setup, we have [an ArXiv dataset](https://marketplace.databricks.com/details/519f6cd1-d9a8-4a06-998d-b6fb58d94565/Databricks_ArXiv-Sample-Articles) that has been brought in from Databricks Marketplace and copied to the user catalog. Let's extract some useful information from one of these PDFs.
# MAGIC
# MAGIC #### Instructions
# MAGIC 1. Navigate to **Agents** in the left side menu and click on it. 
# MAGIC 1. Click on **Use PDFs** under **Information Extraction**. 
# MAGIC 1. Under **Create workflow**
# MAGIC     - Click on the file finder under **Select folder with PDFs or images**
# MAGIC     - Search for **demo_build_agents_vol** and navigate to the subdirectory called **demo_single_pdf**. 
# MAGIC     - Click **Confirm**.
# MAGIC     - Under **Select destination table**, navigate to the schema set up for this lab under **dbacademy**. Click on **All**, then under `dbacademy`, select the schema (it will begin with **labuser**) and click the **Confirm** button. 
# MAGIC     - Change the name of the destination table to **demo_01_single_pdf_parsed**. 
# MAGIC     - Select the SQL warehouse **agent_XS**. If this warehouse is not appearing, you will need to start it under **Compute -> SQL Warehouse** in the left side menu. 
# MAGIC     - Click **Start import**
# MAGIC
# MAGIC This will kickoff a Lakeflow Job automatically that points to a single task (SQL Query). Let's inspect this query for a more comprehensive understanding of what is happening with the automatic parsing.

# COMMAND ----------

# MAGIC %md
# MAGIC ### B1. Inspecting parse_pdfs_to_delta Lakeflow Job
# MAGIC After completing the previous task: 
# MAGIC 1. Navigate to **Jobs & Pipelines** and find the job you just created called **parse_pdfs_to_delta**.
# MAGIC 1. Under the **Recent runs**, click on the latest run. It may be still running or showing a green circle and checkmark. This will take you to the underlying SQL queries being used for the parsing.
# MAGIC
# MAGIC While this job is running, let's take a look at the SQL code. 
# MAGIC > The time it takes for these queries to complete for this query is ~ 2-3 minutes.

# COMMAND ----------

# MAGIC %md
# MAGIC #### B1.1 Define viable extensions for `ai_parse_document()`.
# MAGIC First, it creates a variable called `parse_extensions` that contains the file suffices that should be fed into the parsing logic to come next: 
# MAGIC
# MAGIC ```
# MAGIC DECLARE parse_extensions ARRAY<STRING> DEFAULT array('.pdf', '.jpg', '.jpeg', '.png');
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC #### B1.2 `CREATE TABLE` Statement (Parameterized)
# MAGIC Here we are creating a table with the tablename to be defined via `:destinationTableName`. We will break down the CTEs and final `SELECT` statement mentioned in the following code snippet in the markdown that follows. 
# MAGIC
# MAGIC ```
# MAGIC CREATE TABLE IDENTIFIER(:destinationTableName) AS (
# MAGIC   <CTEs and final SELECT statement>
# MAGIC );
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC #### B1.3 Read Batch Files
# MAGIC Next, we read up to `:limit` files from our volume, which is defined using the parameter `:sourceVolumePath`, and return each file's path and raw binary bytes as `content`: 
# MAGIC ```
# MAGIC WITH all_files AS (
# MAGIC   SELECT path, content
# MAGIC   FROM READ_FILES(:sourceVolumePath, format => 'binaryFile')
# MAGIC   ORDER BY path
# MAGIC   LIMIT INT(:limit)
# MAGIC ),
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC #### B1.4 Split into Parsed and Raw Text Files
# MAGIC Using our variable `parse_extensions` (see **B1.1**), the following splits those files that match suffixes. Anything that match extensions _.pdf_, _.jpg_, _.jpeg_, or _.png_ will have its `content` (in `binaryFile` format) fed to the SQL AI function `ai_parse_document()`. Otherwise, the bytes from `content` are sent to UTF-8 text and `raw_parsed` is left as `NULL`. We will join back to these raw text files later (see **B1.7**). 
# MAGIC ```
# MAGIC parsed_documents AS (
# MAGIC   SELECT path, ai_parse_document(content) AS parsed
# MAGIC   FROM all_files
# MAGIC   WHERE array_contains(parse_extensions,
# MAGIC                        lower(regexp_extract(path, r'(\.[^.]+)$', 1)))
# MAGIC ),
# MAGIC raw_documents AS (
# MAGIC   SELECT path,
# MAGIC          NULL           AS raw_parsed,
# MAGIC          decode(content, 'utf-8') AS text
# MAGIC   FROM all_files
# MAGIC   WHERE NOT array_contains(parse_extensions,
# MAGIC                            lower(regexp_extract(path, r'(\.[^.]+)$', 1)))
# MAGIC ),
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### What is `ai_parse_document()`?
# MAGIC The `ai_parse_document()` function invokes a state-of-the-art generative AI model from Databricks Foundation Model APIs to extract structured content from unstructured documents. You can read more about this function [here](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_parse_document).

# COMMAND ----------

# MAGIC %md
# MAGIC #### B1.5 Explode Parsed Documents
# MAGIC Using `parsed_documents` (see **B1.4**), the following takes the `pages` array from the parser's JSON output, explodes into rows, and pulls out each page's `content`. Note that we see a `try_cast()` SQL function that is using an `ARRAY<VARIANT>` data type. This will be important later when we query this table. 
# MAGIC ```
# MAGIC sorted_page_contents AS (
# MAGIC   SELECT path, page:content AS content
# MAGIC   FROM (
# MAGIC     SELECT path,
# MAGIC            posexplode(try_cast(parsed:document:pages AS ARRAY<VARIANT>))
# MAGIC              AS (page_idx, page)
# MAGIC     FROM parsed_documents
# MAGIC     WHERE parsed:document:pages IS NOT NULL
# MAGIC       AND CAST(parsed:error_status AS STRING) IS NULL
# MAGIC   )
# MAGIC   ORDER BY page_idx
# MAGIC ),
# MAGIC
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC #### B1.6 Reassemble the Document
# MAGIC Group the per-page rows back into a single big text blob per file. 
# MAGIC ```
# MAGIC concatenated AS (
# MAGIC   SELECT path,
# MAGIC          concat_ws('\n\n', collect_list(content)) AS full_content
# MAGIC   FROM sorted_page_contents
# MAGIC   GROUP BY path
# MAGIC ),
# MAGIC
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC #### B1.7 Join to Original Parsed Output
# MAGIC Keep both the full parsed JSON (`raw_parsed`) and the assembled plain-text pages (`text`) together. 
# MAGIC ```
# MAGIC with_raw AS (
# MAGIC   SELECT a.path,
# MAGIC          b.parsed      AS raw_parsed,
# MAGIC          a.full_content AS text
# MAGIC   FROM concatenated a
# MAGIC   JOIN parsed_documents b
# MAGIC     ON a.path = b.path
# MAGIC )
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC #### B1.8 Combine Parsed and Raw Files
# MAGIC This will return three columns in our final table: `path`, `raw_parsed`, and `text`. 
# MAGIC ```
# MAGIC SELECT * FROM with_raw
# MAGIC UNION ALL
# MAGIC SELECT * FROM raw_documents
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC #### B1.9 Sample results
# MAGIC This will select the first 20 rows from our newly created Delta table `:destinationTableName` 
# MAGIC ```
# MAGIC SELECT *
# MAGIC FROM IDENTIFIER(:destinationTableName)
# MAGIC LIMIT 20;
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### B2. How to Flatten `demo_01_single_pdf_parsed`
# MAGIC Now that we understand this SQL query, let's look at the table itself. Recall from the notes above, that a `VARIANT` data type was created. Run the next cell to view the table.

# COMMAND ----------

df = spark.read.table(f'{DA.catalog_name}.{DA.schema_name}.`demo_01_single_pdf_parsed`')
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC We can use SQL to help flatten this table on `raw_parsed`. Let's use a lateral join (`LATERAL`) with `variant_explode()`. 
# MAGIC
# MAGIC #### Using `variant_explode()`
# MAGIC The input is `variantExpr`, which is a `VARIANT` expression, representing a `VARIANT` object or `VARIANT ARRAY`. The output is a set of rows composed of the elements of the `VARIANT ARRAY` or the keys and values of the `VARIANT` object. The columns produced by `variant_explode()` are:
# MAGIC ```
# MAGIC pos INT
# MAGIC key STRING
# MAGIC value VARIANT
# MAGIC ```
# MAGIC
# MAGIC > Read more about `variant_explode()` [here](https://docs.databricks.com/gcp/en/sql/language-manual/functions/variant_explode).

# COMMAND ----------

# MAGIC %md
# MAGIC Run the next cell and view the three new columns we just mentioned: `pos`, `key`, and `value`.

# COMMAND ----------


df = spark.sql(f"""
SELECT
    *
FROM {DA.catalog_name}.{DA.schema_name}.`demo_01_single_pdf_parsed`,
LATERAL variant_explode(raw_parsed:document:elements)
""")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC Let's break down `value` - this contains all the content we care about. Running the next cell will produce a single column called `content`, which are chunks of the underlying PDF.

# COMMAND ----------

df = spark.sql(f"""
               SELECT
               CAST(value:content AS STRING) AS content
               FROM {DA.catalog_name}.{DA.schema_name}.`demo_01_single_pdf_parsed`,
               LATERAL variant_explode(raw_parsed:document:elements)
               """)
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Information Extraction
# MAGIC Agent Bricks supports information extraction and simplifies the process of transforming a large volume of unlabeled text documents into a structured table with extracted information for each document.
# MAGIC
# MAGIC Though Information Extraction leverages automated evaluation capabilities, including MLflow and Agent Evaluation, to enable rapid assessment of the cost-quality tradeoff for your specific extraction task, we will only walk through how to extract information and improve information extraction. 
# MAGIC
# MAGIC #### Understanding Limitations and Requirements for IE Agents
# MAGIC _Keep in mind that this feature is currently in beta_. [Here](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/key-info-extraction#limitations) are some limitations to be aware of when building agents on Databricks. 
# MAGIC
# MAGIC ### Instructions
# MAGIC Using the parsed table, let's create an document-wide information extraction agent. In particular, let's extract the authors and the paper's conclusion from the `text` column. 
# MAGIC 1. Navigate to **Information Extraction** under **Agents** and click **Build**. 
# MAGIC 1. Under **Dataset location**, click the folder finder textbox, locate the table created in the previous section (`demo_01_single_pdf_parsed`) and select **Use this table**.
# MAGIC 1. A new option will appear that asks you to **Select the column containing your text data**. Select the **text** column from the dropdown menu.  
# MAGIC 1. Next, we need to provide a sample of what the JSON response should look like. Navigate to the JSON file called `demo_information_extraction_example.json` in the folder called `json_samples` and copy and paste the contents there into the **Sample output** textbox. Note that when selecting the text column, Databricks will automatically try to infer a schema for you. 
# MAGIC 1. Give the agent a name and click **Create agent** (e.g. _demo-agent_).
# MAGIC 1. This will take you to the **Build** window. Here, you will see two **schema definition** values called **authors** and **paper_conclusions**. These are the same fields defined in the source JSON file you copied from.
# MAGIC 1. Let's update the prompt under **paper_conclusions** to read: _"A textual summary or conclusion of the research findings or paper, represented as a string. Keep your response to 3-5 sentences."_ Here, we are performing prompt engineering to guide our agent to behave in a particular way. 
# MAGIC 1. Select **Save and update** at the bottom of the screen. Notice the agent's response column follows the prompt. 
# MAGIC 1. Finish by selecting **Use your agent** at the bottom of the screen. 
# MAGIC
# MAGIC > Click [here](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/key-info-extraction) to read more about Information Extraction Agents.

# COMMAND ----------

# MAGIC %md
# MAGIC ### C1. Extract Data for All Documents
# MAGIC On the **Use** tab, we see:
# MAGIC 1. Deployed agent endpoint and status
# MAGIC 1. **Extract data for all documents**
# MAGIC 1. **Create DLT pipeline**
# MAGIC 1. **Get a cheaper agent**
# MAGIC
# MAGIC We will close this demonstration with a comment on using each of these items. 
# MAGIC
# MAGIC #### Extract Data for all Document in this Notebook
# MAGIC If you click on **Start extraction** on the **Extract data for all documents** tile, you will be taken to a SQL query similar to the next cell. We are only using one PDF in our source folder. We can simply copy and paste this code for demonstration purposes down below (we have already done this). 
# MAGIC
# MAGIC #### Instructions
# MAGIC 1. Run the next cell to use the Databricks SDK to find the name of the endpoint you created.
# MAGIC 1. Run the subsequent cell to produce the summary of the entire paper as a single row and column.
# MAGIC > Again, this is basically the same code you get when you generate the SQL code from selecting **Extract data for all documents** on the **Use** tab under **Agents**. It has been modified to only get the summary of the paper. Running it in the notebook uses Serverless compute, while SQL Warehouse compute is used when running from the **SQL Editor**. This is for demonstration purposes only.

# COMMAND ----------

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

for ep in w.serving_endpoints.list():
    if ep.creator == DA.username:
        user_endpoint = f"'{ep.name}'"
        print(f"Your endpoint as a string: {user_endpoint}")
        break # This till grab the latest endpoint created in case you have other agents already deployed.

# COMMAND ----------

df = spark.sql(f"""
WITH query_results AS (
  SELECT
    `text` AS input,
    ai_query(
      {user_endpoint},
      input,
      failOnError => false
    ) AS response
  FROM (
    SELECT `text` 
    FROM {DA.catalog_name}.{DA.schema_name}.`demo_01_single_pdf_parsed`
    LIMIT 20
  )
)
SELECT
  value
FROM query_results,
LATERAL variant_explode(try_parse_json(try_variant_get(response.result, '$', 'string')))
WHERE key == 'paper_conclusions'""")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### C2. (Optional) Building a Lakeflow Declarative Pipeline 
# MAGIC If you are familiar with [Lakeflow Declarative Pipelines](https://www.databricks.com/product/data-engineering/lakeflow-declarative-pipelines) (FKA Delta Live Tables or DLTs), then you will be comfortable with this feature. 
# MAGIC #### Instructions
# MAGIC 1. Navigate back to the **Use** tab in your deployed Information Extraction Agent. 
# MAGIC 1. Click on **Create Pipeline**. 
# MAGIC 1. You will be taken to a new graph with a single task that will create a streaming table. Click on the task and investigate the source code on the right. Notice this is basically the same as the query we have above, but has been pre-appended with the `CREATE OR REFRESH STREAM TABLE` logic. 
# MAGIC 1. Navigate back to the pipeline UI and click **Start** at the top right. This will kickoff the run. 
# MAGIC 1. Navigate to the catalog and schema within this Vocareum lab environment and after a few moments you will see the streaming table (note you may need to reload the page). 
# MAGIC
# MAGIC You can now use this as a starting point for your AI workloads!
# MAGIC #### A Deeper Dive on Lakeflow Declarative Pipelines
# MAGIC If you are interested in learning more about Lakeflow Declarative Pipelines, please see our other [courses](https://www.databricks.com/training/catalog?search=lakeflow+declarative+pipelines).

# COMMAND ----------

# MAGIC %md
# MAGIC ### C3. Optimizing the Agent (Outside the Scope of this Demo) 
# MAGIC When you select **Optimize** on the **Use** tab, Databricks compares multiple different optimization strategies to build and recommend an optimized agent. These strategies include Foundation Model Fine-tuning which uses [Databricks Geos](https://docs.databricks.com/aws/en/resources/databricks-geos) (which are groups of data center regions that Databricks groups together to give customers predictability and transparency regarding where your data is processed.).
# MAGIC > Note you will not be able to click the **Optimize** button in this demo because our dataset is too small. 
# MAGIC #### Requirements
# MAGIC Using an optimized agent goes beyond the scope of this demonstration, but there are some requirements here:
# MAGIC - Databricks requires a minimum of 75 documents for optimization to take place
# MAGIC - At least 1k documents are recommend for better results. The reason for this is that when more documents are added, the knowledge base that the agent can learn from increases, which improves agent quality and its extraction accuracy. 
# MAGIC - Optimization takes ~ 1 hour and will block any changes to the active agent during that time.

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusions and Summary
# MAGIC In this demo, you learned how to parse PDFs and understand declarative code Databricks provides to leverage SQL AI functions like `ai_parse_document()` and `ai_query()`. You learned how to leverage Databricks' no-code agents to extract information from parsed PDFs by using Agent Bricks.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
