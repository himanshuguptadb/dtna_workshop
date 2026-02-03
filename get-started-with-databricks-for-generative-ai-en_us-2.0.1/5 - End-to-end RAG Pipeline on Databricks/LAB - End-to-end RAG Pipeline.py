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
# MAGIC # LAB - End-to-end RAG Pipeline
# MAGIC
# MAGIC In this lab, you will build a Retrieval-Augmented Generation (RAG) pipeline on Databricks using various generative AI tools. The RAG pipeline will leverage Databricks documentation as an external knowledge base to answer questions related to Databricks.
# MAGIC
# MAGIC **Lab Outline:**
# MAGIC
# MAGIC - **Task 1**: Create a vector search index.
# MAGIC - **Task 2**: Build the RAG model.
# MAGIC - **Task 3**: Register the RAG model.
# MAGIC - **Task 4**: Evaluate the RAG model.
# MAGIC - **Task 5**: Analyze and interpret the evaluation results.
# MAGIC - **Task 6**: Deploy the model.
# MAGIC - **Task 7**: Test the model using the Review App.
# MAGIC
# MAGIC **📌 Your Task: In this lab, your task is to replace `<FILL_IN>` sections with appropriate code.**

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
# MAGIC ## Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC * To run this notebook, you need to use one of the following Databricks runtime(s): **17.3.x-cpu-ml-scala2.13**

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC Install required libraries.

# COMMAND ----------

# MAGIC %pip install -qqq -U databricks-sdk databricks-langchain databricks-vectorsearch==0.61 langchain==0.3.27 'mlflow-skinny[databricks]>=3.4.0'
# MAGIC %restart_python

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-Lab

# COMMAND ----------

# Variables to use in this notebook
vs_endpoint_prefix = "vs_endpoint_"
vs_endpoint_name = vs_endpoint_prefix+str(get_fixed_integer(DA.unique_name("_")))
vs_source_table_name = f"{DA.catalog_name}.{DA.schema_name}.databricks_doc"
vs_index_table_name = f"{DA.catalog_name}.{DA.schema_name}.databricks_doc_index"

model_name = f"{DA.catalog_name}.{DA.schema_name}.getstarted_genai_lab"

print(f"=== Variables that you will need/use in this lab === \n")
print(f"Catalog Name                : {DA.catalog_name}\n")
print(f"Schema Name                 : {DA.schema_name}\n")
print(f"Model Name                  : {model_name}\n")
print(f"Vector Search Endpoint      : {vs_endpoint_name}\n")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lab Preparation
# MAGIC
# MAGIC Before you start the lab, run the following cells. The first cell imports required libraries and defines variables that will be used during this lab. The second cell reads dataset from the source and saves it as a Delta table.

# COMMAND ----------

import time
from operator import itemgetter
import mlflow
import pandas as pd
from mlflow.models import infer_signature
from mlflow.models.resources import (
    DatabricksVectorSearchIndex
)
import langchain
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

import databricks.vector_search
from databricks.vector_search.client import VectorSearchClient
from databricks_langchain import ChatDatabricks, DatabricksVectorSearch
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import EndpointStateReady, EndpointStateConfigUpdate
from databricks import agents

# COMMAND ----------

# Read dataset and save it as delta table
df = spark.read.load(f"{DA.paths.datasets.docs}/files")
df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(vs_source_table_name)
spark.sql(f"ALTER TABLE {vs_source_table_name} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Problem
# MAGIC
# MAGIC Large Language Models (LLMs) can generate **hallucinated or outdated responses** when they lack sufficient knowledge about the question being asked. For instance, in the chatbot example below, when querying about model management in Unity Catalog on Databricks, part of the generated response is hallucinated—particularly the section on "lifecycle management."
# MAGIC
# MAGIC **To address this issue, you will use Databricks documentation as contextual information for the LLM, enabling it to provide more accurate and reliable answers.**

# COMMAND ----------

prompt_no_context = PromptTemplate.from_template(
    """You are Databricks expert! Don't answer the questions that you don't know. Answer following question:
    Question: {question}

    Answer:
    """)

model = ChatDatabricks(endpoint="databricks-meta-llama-3-3-70b-instruct", max_tokens = 500, temperature=0.1)

chain_no_context = (prompt_no_context | model | StrOutputParser())
answer = chain_no_context.invoke({"question": "How to move a model from dev stage to production stage in Unity Catalog"})
print(answer)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 1: Create A Vector Search Index
# MAGIC
# MAGIC Create a Vector Search index that will use Databricks documentation table that we created above as source table. Below are some other configurations that you need to use:
# MAGIC
# MAGIC * Embedding model to use: **`databricks-gte-large-en`**
# MAGIC
# MAGIC * Columns: **`id`(primary key), `content`(source column)**

# COMMAND ----------

Check if the VS endpoint is ready.
if not is_vs_endpoint_ready(vs_endpoint_name):
    raise Exception("VS Endpoint is not ready! It must be created before moving to next steps")

Create or sync the index
vsc = VectorSearchClient(disable_notice=True)
if not index_exists(vsc, vs_endpoint_name, vs_index_table_name):
    print(f"Creating index {vs_index_table_name} on endpoint {vs_endpoint_name}...")

    vsc.<FILL_IN>
else:
    # Trigger a sync to update our vs content with the new data saved in the table
    vsc.<FILL_IN>

Let's wait for the index to be ready and all our embeddings to be created and indexed
wait_for_index_to_be_ready(vsc, vs_endpoint_name, vs_index_table_name)

# COMMAND ----------

# MAGIC %skip
# MAGIC # Check if the VS endpoint is ready.
# MAGIC if not is_vs_endpoint_ready(vs_endpoint_name):
# MAGIC     raise Exception("VS Endpoint is not ready! It must be created before moving to next steps")
# MAGIC
# MAGIC # Create or sync the index
# MAGIC vsc = VectorSearchClient(disable_notice=True)
# MAGIC if not index_exists(vsc, vs_endpoint_name, vs_index_table_name):
# MAGIC     print(f"Creating index {vs_index_table_name} on endpoint {vs_endpoint_name}...")
# MAGIC
# MAGIC     vsc.create_delta_sync_index(
# MAGIC         endpoint_name=vs_endpoint_name,
# MAGIC         index_name=vs_index_table_name,
# MAGIC         source_table_name=vs_source_table_name,
# MAGIC         pipeline_type="TRIGGERED",
# MAGIC         primary_key="id",
# MAGIC         embedding_source_column="content",
# MAGIC         embedding_model_endpoint_name="databricks-gte-large-en"
# MAGIC     )
# MAGIC else:
# MAGIC     # Trigger a sync to update our vs content with the new data saved in the table
# MAGIC     vsc.get_index(vs_endpoint_name, vs_index_table_name).sync()
# MAGIC
# MAGIC # Let's wait for the index to be ready and all our embeddings to be created and indexed
# MAGIC wait_for_index_to_be_ready(vsc, vs_endpoint_name, vs_index_table_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 2: Build a RAG Model
# MAGIC
# MAGIC In this task, you will build a Retrieval-Augmented Generation (RAG) model that uses the Vector Search index you created earlier. The agent code required for this step is already provided for you in the `agent.py` file—please review this file to understand the implementation. You do not need to write or modify any LangChain code, as LangChain is not in scope for this course.
# MAGIC
# MAGIC Complete the following items:
# MAGIC
# MAGIC - Enable MLflow tracing for the chain to capture and log model interactions.
# MAGIC - Query the agent after importing it
# MAGIC
# MAGIC All necessary agent logic is handled in `agent.py`. Focus on configuring and running the RAG model as described above.

# COMMAND ----------

Enable MLflow tracing for the chain
mlflow.<FILL_IN>

Set environment variable for the vector search index
import os
os.environ["VS_INDEX_NAME"] = <FILL_IN>

Load and test the agent
from agent import AGENT

Test the agent
user_input = "How to move a model from dev stage to production stage in Unity Catalog"
request = {
    "input": [
        {"role": "user", "content": user_input}
    ]
}
resp = AGENT.<FILL_IN>
print(f"\n=== Agent Response === \n{resp}")

# COMMAND ----------

# MAGIC %skip
# MAGIC # Enable MLflow tracing for the chain
# MAGIC mlflow.langchain.autolog()
# MAGIC
# MAGIC # Set environment variable for the vector search index
# MAGIC import os
# MAGIC os.environ["VS_INDEX_NAME"] = vs_index_table_name
# MAGIC
# MAGIC # Load and test the agent
# MAGIC from agent import AGENT
# MAGIC
# MAGIC # Test the agent
# MAGIC user_input = "How to move a model from dev stage to production stage in Unity Catalog"
# MAGIC request = {
# MAGIC     "input": [
# MAGIC         {"role": "user", "content": user_input}
# MAGIC     ]
# MAGIC }
# MAGIC resp = AGENT.predict(request)
# MAGIC print(f"\n=== Agent Response === \n{resp}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 3: Register the RAG Model
# MAGIC
# MAGIC After building the model, you will store it in the model registry for future use. Complete the following items in this task:
# MAGIC
# MAGIC - Set the model registry to **Unity Catalog**.
# MAGIC
# MAGIC - Log the model with **necessary configurations such as "signature", "input example", "pip requirements", and "resources".**

# COMMAND ----------

Set model registry URI to Unity Catalog
mlflow.<FILL_IN>

Set the agent for MLflow Models-from-Code
mlflow.models.<FILL_IN>

Log the assembled RAG model in Model Registry with Unity Catalog
with mlflow.start_run(run_name="genai_gs_lab") as run:
    model_info = mlflow.<FILL_IN>

Register the model with the name we defined in the beginning of the notebook
model_uri = f"runs:/{run.info.run_id}/{model_info.name}"
model_version = mlflow.<FILL_IN>
print(f"Model registered with name: {model_name} and version: {model_version.version}")

# COMMAND ----------

# MAGIC %skip
# MAGIC # Set model registry URI to Unity Catalog
# MAGIC mlflow.set_registry_uri("databricks-uc")
# MAGIC
# MAGIC # Set the agent for MLflow Models-from-Code
# MAGIC mlflow.models.set_model(AGENT)
# MAGIC
# MAGIC # Log the assembled RAG model in Model Registry with Unity Catalog
# MAGIC with mlflow.start_run(run_name="genai_gs_lab") as run:
# MAGIC     model_info = mlflow.pyfunc.log_model(
# MAGIC         name="agent",
# MAGIC         python_model="agent.py",
# MAGIC         pip_requirements=[
# MAGIC             f"langchain=={langchain.__version__}",
# MAGIC             f"databricks-vectorsearch=={databricks.vector_search.__version__}",
# MAGIC             f"databricks_langchain",
# MAGIC             f"mlflow=={mlflow.__version__}"
# MAGIC         ],
# MAGIC         resources=[
# MAGIC             DatabricksVectorSearchIndex(index_name=vs_index_table_name)
# MAGIC         ]
# MAGIC     )
# MAGIC
# MAGIC # Register the model with the name we defined in the beginning of the notebook
# MAGIC model_uri = f"runs:/{run.info.run_id}/{model_info.name}"
# MAGIC model_version = mlflow.register_model(model_uri, model_name)
# MAGIC print(f"Model registered with name: {model_name} and version: {model_version.version}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 4: Evaluate the RAG Model
# MAGIC
# MAGIC Does your model perform well? In this task, you will evaluate the model using the Mosaic AI Agent Evaluation Framework. This framework includes built-in evaluation metrics, and you will also define a custom metric.
# MAGIC
# MAGIC - A simple evaluation dataset is provided. **What other fields could be included in the evaluation dataset?**
# MAGIC
# MAGIC - Define a custom metric to assess whether the retrieved documentation contains code. Use **`meta-llama-3-3`** as the LLM-as-Judge model.
# MAGIC
# MAGIC - Run the evaluation and ensure to **log it in MLflow**. **The evaluation run should include the custom metric you defined**.
# MAGIC

# COMMAND ----------

display(DA.eval_set)

# COMMAND ----------

model_uri = f"models:/{model_name}/1"

Load the model for evaluation
model = mlflow.<FILL_IN>

Predict function expected by mlflow.genai.evaluate()
@mlflow.trace
def predict_fn(messages):
    """
    messages: list of {role, content}
    Returns: assistant text (str) for scorers.
    """
    out = model.predict({"input": messages})

    # Databricks Responses shape: {"object":"response","output":[{message...}]}
    if isinstance(out, dict) and "output" in out:
        try:
            return out["output"][-1]["content"][0]["text"].strip()
        except Exception:
            pass  # fall through

    # Older shape: list of message dicts
    if isinstance(out, list):
        try:
            return out[-1]["content"][0]["text"].strip()
        except Exception:
            pass

    # Fallback: return as string
    return str(out)

Run the evaluation process
with mlflow.start_run(run_name="genai_gs_lab_eval"):
    eval_results = <FILL_IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC from mlflow.genai import evaluate
# MAGIC from mlflow.genai.scorers import Guidelines, RelevanceToQuery, Safety
# MAGIC
# MAGIC model_uri = f"models:/{model_name}/1"
# MAGIC
# MAGIC # Load the model for evaluation
# MAGIC model = mlflow.pyfunc.load_model(model_uri)
# MAGIC
# MAGIC # Predict function expected by mlflow.genai.evaluate()
# MAGIC @mlflow.trace
# MAGIC def predict_fn(messages):
# MAGIC     """
# MAGIC     messages: list of {role, content}
# MAGIC     Returns: assistant text (str) for scorers.
# MAGIC     """
# MAGIC     out = model.predict({"input": messages})
# MAGIC
# MAGIC     # Databricks Responses shape: {"object":"response","output":[{message...}]}
# MAGIC     if isinstance(out, dict) and "output" in out:
# MAGIC         try:
# MAGIC             return out["output"][-1]["content"][0]["text"].strip()
# MAGIC         except Exception:
# MAGIC             pass  # fall through
# MAGIC
# MAGIC     # Older shape: list of message dicts
# MAGIC     if isinstance(out, list):
# MAGIC         try:
# MAGIC             return out[-1]["content"][0]["text"].strip()
# MAGIC         except Exception:
# MAGIC             pass
# MAGIC
# MAGIC     # Fallbacks
# MAGIC     if isinstance(out, str):
# MAGIC         return out.strip()
# MAGIC     if isinstance(out, dict):
# MAGIC         for k in ("answer", "response", "text", "output"):
# MAGIC             v = out.get(k)
# MAGIC             if isinstance(v, str):
# MAGIC                 return v.strip()
# MAGIC
# MAGIC     return str(out).strip()
# MAGIC
# MAGIC
# MAGIC # Guidelines scorer for has_code (boolean pass/fail)
# MAGIC has_code_guidelines = Guidelines(
# MAGIC     name="has_code",
# MAGIC     guidelines="""The response must include code samples."""
# MAGIC )
# MAGIC
# MAGIC # Run the evaluation process
# MAGIC with mlflow.start_run(run_name="genai_gs_lab_eval") as eval_run:
# MAGIC     eval_results = evaluate(
# MAGIC         data=DA.eval_set,
# MAGIC         predict_fn=predict_fn,
# MAGIC         scorers=[
# MAGIC             RelevanceToQuery(),
# MAGIC             Safety(),
# MAGIC             has_code_guidelines
# MAGIC         ]
# MAGIC     )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 5: Show and Interpret Evaluation Results
# MAGIC
# MAGIC Display the evaluation results in a table. Review the results using the MLflow UI.
# MAGIC
# MAGIC - What steps do you need to take to view the evaluation table?
# MAGIC - How can you compare model and system metrics in the UI?
# MAGIC - What information is available for "retrieval" and "response" metrics?
# MAGIC - How can you check if the rationale for the "custom metric" is correct?
# MAGIC
# MAGIC

# COMMAND ----------

Show evaluation metrics summary
display(<FILL_IN>)

# COMMAND ----------

# MAGIC %skip
# MAGIC # Show evaluation metrics summary
# MAGIC display(eval_results.tables['eval_results'])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 6: Serve the Model
# MAGIC
# MAGIC If you are satisfied with the model, it's time to deploy it! In this step, you will serve the model using the Agents Framework.
# MAGIC
# MAGIC - Ensure that the **`scale_to_zero`** setting is enabled.

# COMMAND ----------

Deploy the model with the agent framework
deployment_info = agents.deploy(
    <FILL_IN>, 
    model_version=<FILL_IN>,
    scale_to_zero=<FILL_IN>,
    environment_vars=<FILL_IN>
)

Wait for the Review App and deployed model to be ready
w = WorkspaceClient()
print("\nWaiting for endpoint to deploy.  This can take 15 - 20 minutes.", end="")

while ((w.serving_endpoints.get(deployment_info.endpoint_name).state.ready == EndpointStateReady.NOT_READY) or (w.serving_endpoints.get(deployment_info.endpoint_name).state.config_update == EndpointStateConfigUpdate.IN_PROGRESS)):
    print(".", end="")
    time.sleep(30)

print("\nThe endpoint is ready!", end="")

# COMMAND ----------

# MAGIC %skip
# MAGIC # Deploy the model with the agent framework, passing VS_INDEX_NAME as an environment variable
# MAGIC deployment_info = agents.deploy(
# MAGIC     model_name, 
# MAGIC     model_version=1,
# MAGIC     scale_to_zero=True,
# MAGIC     environment_vars={"VS_INDEX_NAME": vs_index_table_name}
# MAGIC )
# MAGIC
# MAGIC
# MAGIC # Wait for the Review App and deployed model to be ready
# MAGIC w = WorkspaceClient()
# MAGIC print("\nWaiting for endpoint to deploy.  This can take 15 - 20 minutes.", end="")
# MAGIC
# MAGIC while ((w.serving_endpoints.get(deployment_info.endpoint_name).state.ready == EndpointStateReady.NOT_READY) or (w.serving_endpoints.get(deployment_info.endpoint_name).state.config_update == EndpointStateConfigUpdate.IN_PROGRESS)):
# MAGIC     print(".", end="")
# MAGIC     time.sleep(30)
# MAGIC
# MAGIC print("\nThe endpoint is ready!", end="")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 7: Test the Model with Review App
# MAGIC
# MAGIC When the deployment process is completed, complete the following steps.
# MAGIC
# MAGIC * Display the **"Endpoint URL"** and **"Review App URL"**.
# MAGIC
# MAGIC * Use Review App to ask questions and review the response.
# MAGIC
# MAGIC * Provide feedback for the generated response.

# COMMAND ----------

print(f"Endpoint URL    : {<FILL_IN>}")
print(f"Review App URL  : {<FILL_IN>}")

# COMMAND ----------

# MAGIC %skip
# MAGIC print(f"Endpoint URL    : {deployment_info.endpoint_url}")
# MAGIC print(f"Review App URL  : {deployment_info.review_app_url}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC In this lab, you built and deployed a generative AI model that uses a knowledge base to answer questions accurately. First, you created a Vector Search index based on the base documentation dataset. Then, you built a RAG pipeline and registered it in the model registry. After evaluating the model using common model metrics, system metrics, and custom metrics, you reviewed the evaluation results. In the final section, the model was served and tested via the Review App. Upon successfully completing this lab, you should be able to build, deploy, and evaluate a generative AI model using the Databricks Mosaic AI platform.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
