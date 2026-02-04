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
# MAGIC ## DEMO - Build and Register a RAG Model
# MAGIC
# MAGIC A Retrieval-Augmented Generation (RAG) model is a widely used architecture for generative AI applications, particularly when contextual information needs to accompany the prompt. **In this demo, we will construct a RAG pipeline and register it in the Unity Catalog model registry.**
# MAGIC
# MAGIC The RAG pipeline will function as a simple **product design chatbot**. As contextual information, we will provide product descriptions that have previously **listed on Etsy website**. Please note that the dataset **we will use is publicly available, and the large language model (LLM) might already include this data in its training set**. Consequently, the quality of responses with and without contextual data might not differ significantly. In a real-world scenario, the contextual data would include information that is new to the LLM.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC By the end of this demo, you will be able to:
# MAGIC
# MAGIC 1. Inspect the Vector Search endpoint and index using the Databricks UI.
# MAGIC 2. Configure a Vector Search index using an existing Delta table.
# MAGIC 3. Retrieve documents from the vector store using similarity search.
# MAGIC 4. Assemble a RAG pipeline by integrating multiple components.
# MAGIC 5. Register a RAG pipeline in the Unity Catalog Model Registry.

# COMMAND ----------

# MAGIC %md
# MAGIC ## REQUIRED - SELECT CLASSIC COMPUTE
# MAGIC Before executing cells in this notebook, please select your classic compute cluster in the lab. Be aware that **Serverless** is enabled by default.
# MAGIC
# MAGIC Follow these steps to select the classic compute cluster:
# MAGIC 1. Navigate to the top-right of this notebook and click the drop-down menu to select your cluster. By default, the notebook will use **Serverless**.
# MAGIC
# MAGIC 2. If your cluster is available, select it and continue to the next cell. If the cluster is not shown:
# MAGIC
# MAGIC    - Click **More** in the drop-down.
# MAGIC
# MAGIC    - In the **Attach to an existing compute resource** window, use the first drop-down to select your unique cluster.
# MAGIC
# MAGIC **NOTE:** If your cluster has terminated, you might need to restart it in order to select it. To do this:
# MAGIC
# MAGIC 1. Right-click on **Compute** in the left navigation pane and select *Open in new tab*.
# MAGIC
# MAGIC 2. Find the triangle icon to the right of your compute cluster name and click it.
# MAGIC
# MAGIC 3. Wait a few minutes for the cluster to start.
# MAGIC
# MAGIC 4. Once the cluster is running, complete the steps above to select your cluster.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Requirements
# MAGIC
# MAGIC Before starting, ensure you meet the following requirements:
# MAGIC
# MAGIC - This notebook must be run on one of the following Databricks runtimes: **17.3.x-cpu-ml-scala2.13**

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Classroom Setup
# MAGIC
# MAGIC Let's set up your environment! This will install the libraries and datasets you need for the demo. Running the next cell will make sure everything is ready to go.

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-02

# COMMAND ----------

# MAGIC %md
# MAGIC This script defines key variables for the Vector Search endpoint, source table, and index table. These variables will be used throughout the demo to reference resources in your workspace.

# COMMAND ----------

# assign vs search endpoint by username
#vs_endpoint_prefix = "vs_endpoint_"
vs_endpoint_name = "agent_bootcamp_endpoint"
vs_source_table_name = f"{DA.catalog_name}.{DA.schema_name}.product_text"
vs_index_table_name = f"{DA.catalog_name}.{DA.schema_name}.product_embeddings"

print(f"=== Variables that you will need for this demo === \n")
print(f"Catalog Name                : {DA.catalog_name}\n")
print(f"Schema Name                 : {DA.schema_name}\n")
print(f"Assigned VS endpoint name   : {vs_endpoint_name} \n")
print(f"VS source table name        : {vs_source_table_name} \n")
print(f"VS index table name         : {vs_index_table_name } \n")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Demo Overview
# MAGIC
# MAGIC The initial component of this demonstration is the **retrieval component**. Based on the input query, we will search for and retrieve similar product descriptions.
# MAGIC
# MAGIC Next, we will construct the entire pipeline using LangChain. **Please note that LangChain is not within the scope of this course. For more information, we recommend referring to the "Generative AI Engineering with Databricks" course.**
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Dataset
# MAGIC
# MAGIC We will use a real-world product dataset from Databricks Marketplace. For this demo, we focus on the product title and description columns, which are most useful for finding similar products.

# COMMAND ----------

display(spark.sql(f"SELECT * FROM {vs_source_table_name}"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create and Test Vector Index
# MAGIC
# MAGIC Now, let's make it easy for our model to find relevant product information! We'll create a Vector Search index, which helps us quickly search for similar product descriptions. Once the index is ready, we'll test it with a sample query.
# MAGIC
# MAGIC After testing the index, we will move on to the next step, where we will analyze the results and refine our search capabilities.
# MAGIC
# MAGIC **🚨IMPORTANT: Vector Search endpoints must be created before running the rest of the demo. These are already created for you in Databricks Lab environment.**

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating a Vector Index via UI
# MAGIC
# MAGIC
# MAGIC **Steps to Create a Vector Index:**
# MAGIC
# MAGIC - Navigate to **Catalog** from the left panel and select your course catalog. 
# MAGIC
# MAGIC - Choose your schema. Schema name is printed in the top of the notebook. 
# MAGIC
# MAGIC - Select the **`product_text`** table created in the previous step. You can find all resource names at the top of this notebook.
# MAGIC
# MAGIC - In the top right corner, click **"Create"** and then **"Vector search index"**.
# MAGIC
# MAGIC - Enter **`product_embeddings`** as the index name.
# MAGIC
# MAGIC - Choose **`id`** as the primary key.
# MAGIC
# MAGIC - Choose `document` field as column(s) to sync.
# MAGIC
# MAGIC - For embedding source, select **"compute embeddings"**:
# MAGIC   - Choose **`document` column** as the source column.
# MAGIC   - Select **`databricks-gte-large-en`** as the embedding model. Embedding creation will be **managed** by Databricks which means we don't need to manually compute embeddings.
# MAGIC - Select the endpoint assigned to you. Refer to the top of this notebook for details on the VS endpoint.  
# MAGIC
# MAGIC - Set sync mode to **"Triggered"**.
# MAGIC
# MAGIC - Finally, click the **"Create"** button.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### (Alternative) Creating a Vector Index via API 
# MAGIC
# MAGIC For simplicity, we created the vector index using the UI. However, this process can also be accomplished programmatically using the `databricks-sdk`. For more detailed instructions, please refer to [documentation page](https://docs.databricks.com/en/generative-ai/create-query-vector-search.html#create-index-using-the-python-sdk).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Testing the Index: Search for Products Similar to the Query
# MAGIC
# MAGIC Before building the RAG pipeline, let's check if the index is ready. We will use `similarity_search` function to search for products that are similar to the query text.

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient(disable_notice=True)

question = "handmade lamp with remote control"

try:
    # get index created in the previous step
    index = vsc.get_index(vs_endpoint_name, vs_index_table_name)

    # search for similar documents
    results = index.similarity_search(
        query_text = question,
        columns=["document"],
        num_results=4
    )

    # show the results
    docs = results.get("result", {}).get("data_array", [])
    pprint(docs)

except Exception as e:
    print(f"Error occurred while loading the index. Did you create an index in the previous step?: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC **❓ Question:** If you receive multiple similar documents, how would you determine which ones to utilize as context for your model? Would you select the top two documents, or would you employ a different approach to identify the most significant ones?

# COMMAND ----------

# MAGIC %md
# MAGIC ## Enable MLflow Tracing
# MAGIC
# MAGIC Before we build our RAG pipeline, let's turn on MLflow tracing. This helps us automatically track and log what happens in our pipeline, making it easier to review and improve our work later. 
# MAGIC
# MAGIC **💡 Note: MLflow logging is enabled by default, but we'll show how to enable it here for learning purposes.**

# COMMAND ----------

import mlflow
mlflow.langchain.autolog()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Build a RAG Model
# MAGIC
# MAGIC Now it's time to put everything together! We'll build a simple RAG (Retrieval-Augmented Generation) pipeline that uses the documents we found with Vector Search to help answer questions. This makes our model smarter by giving it extra context.
# MAGIC
# MAGIC **⚠️ Notice:** You must pass the correct VS index name as environment variable. It is used in `agent.py` file to access the index.

# COMMAND ----------

import os
os.environ["VS_INDEX_NAME"] = vs_index_table_name

# COMMAND ----------

# Load the agent code from the agent.py file. This approach allows you to modularize the agent logic and reuse it for deployment or further development.
from agent import AGENT

user_input = "Create a concise title and 250-word description for a handmade lamp with remote dimming."
request = {
    "input": [
        {"role": "user", "content": user_input}
    ]
}
resp = AGENT.predict(request)
print(resp)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Register the RAG Model to Unity Catalog
# MAGIC
# MAGIC Once your RAG pipeline is working, you can register it in Unity Catalog. **This makes it easy to manage, share, and deploy your model later.** Registering your model is a best practice for keeping your work organized and ready for production.

# COMMAND ----------

import mlflow
from mlflow.models.resources import (
    DatabricksVectorSearchIndex
)
from mlflow.models import infer_signature
from pkg_resources import get_distribution

# Set Model Registry URI to Unity Catalog
mlflow.set_registry_uri("databricks-uc")

model_name = f"{DA.catalog_name}.{DA.schema_name}.getstarted_genai_retrevial_demo"

# Set the agent
mlflow.models.set_model(AGENT)

# Register the assembled RAG model in Model Registry with Unity Catalog
with mlflow.start_run(run_name="genai_gs_demo_02_01") as run:
    model_info = mlflow.pyfunc.log_model(
        name="agent",
        python_model="agent.py",
        pip_requirements=[
            f"langchain=={get_distribution('langchain').version}",
            f"databricks-vectorsearch=={get_distribution('databricks-vectorsearch').version}",
            f"databricks_langchain=={get_distribution('databricks_langchain').version}",
            f"mlflow=={get_distribution('mlflow').version}"
        ],
        resources=[
            DatabricksVectorSearchIndex(index_name=vs_index_table_name)
        ]
    )
model_uri = f"runs:/{run.info.run_id}/{model_info.name}"
model_version = mlflow.register_model(model_uri, model_name)
print(f"Model registered with name: {model_name} and version: {model_version.version}")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC **🚨Notice:** Do not delete the catalog or tables created in this demo. You will need them for upcoming exercises.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this demo, we:
# MAGIC
# MAGIC 1. Created a managed vector search index using a Delta table and verified retrieval of relevant product descriptions.
# MAGIC 2. Built a RAG pipeline that integrates Vector Search for context retrieval and a generative model for response generation.
# MAGIC 3. Used an agent-as-code approach by defining the agent logic in the `agent.py` file, enabling modular development and easy deployment.
# MAGIC 4. Registered the RAG pipeline in the Unity Catalog Model Registry, making it available for versioning, management, and production deployment.
# MAGIC
# MAGIC This modular, agent-as-code workflow allows you to maintain, test, and deploy your RAG solutions efficiently using Databricks best practices. In the next demos, you will learn how to evaluate and productionize your registered RAG model.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
