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
# MAGIC # DEMO - Real-time Deployment with Model Serving
# MAGIC
# MAGIC In this demo, we will serve the model stored in the model registry using Mosaic Model Serving. We will utilize the Agent Framework to serve the models. When models are served with the Agent Framework, an app called Review App is automatically deployed alongside the model, allowing you to interact with the model and gather human feedback on its responses.
# MAGIC
# MAGIC ### Learning Objectives
# MAGIC
# MAGIC By the end of this demo, you will be able to:
# MAGIC
# MAGIC 1. Deploy a model using the Agent Framework.
# MAGIC 2. Interact with the deployed model using the Review App.
# MAGIC 3. Collect and review human feedback on model responses.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Select Classic Compute
# MAGIC
# MAGIC Before executing cells in this notebook, select your classic compute cluster. Note that Serverless is enabled by default.
# MAGIC
# MAGIC Follow these steps to select the classic compute cluster:
# MAGIC 1. Navigate to the top-right of this notebook and click the drop-down menu to select your cluster. By default, the notebook will use Serverless.
# MAGIC 2. If your cluster is available, select it and continue to the next cell. If the cluster is not shown:
# MAGIC    1. Click More in the drop-down.
# MAGIC    2. In the Attach to an existing compute resource window, use the first drop-down to select your unique cluster.
# MAGIC 3. If your cluster has terminated, you may need to restart it:
# MAGIC    1. Right-click on Compute in the left navigation pane and select Open in new tab.
# MAGIC    2. Find the triangle icon to the right of your compute cluster name and click it.
# MAGIC    3. Wait a few minutes for the cluster to start.
# MAGIC    4. Once the cluster is running, complete the steps above to select your cluster.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC - To run this notebook, you must use one of the following Databricks runtimes: **17.3.x-cpu-ml-scala2.13**

# COMMAND ----------

# MAGIC %md
# MAGIC ### Classroom Setup
# MAGIC
# MAGIC To set up the classroom environment, please install the required libraries and datasets as specified in the project documentation.

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-03

# COMMAND ----------

# MAGIC %md
# MAGIC ### Other Conventions
# MAGIC
# MAGIC Throughout this demo, the object `DA` is used. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Please run the code block below to display these details:

# COMMAND ----------

model_name = f"{DA.catalog_name}.{DA.schema_name}.getstarted_genai_retrevial_demo"
vs_index_table_name = f"{DA.catalog_name}.{DA.schema_name}.product_embeddings"

print(f"=== Variables that you will need for this demo === \n")
print(f"Catalog Name                : {DA.catalog_name}\n")
print(f"Schema Name                 : {DA.schema_name}\n")
print(f"RAG Registered Model        : {model_name} \n")
print(f"VS index table name         : {vs_index_table_name } \n")

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Serve the Model with Agent Framework
# MAGIC
# MAGIC This section demonstrates how to serve a model from the model registry using Mosaic Model Serving and the Agent Framework. When models are served with the Agent Framework, a Review App is automatically deployed alongside the model, allowing you to interact with the model and gather human feedback on its responses.
# MAGIC
# MAGIC **Note:** This step is intended for the course instructor only. If you are using your own environment, you may comment out the cells and run them to deploy the model and access the Review App.

# COMMAND ----------

import time
import mlflow
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import EndpointStateReady, EndpointStateConfigUpdate
from databricks import agents

# Deploy the model with the agent framework, passing VS_INDEX_NAME as an environment variable
deployment_info = agents.deploy(
    model_name, 
    model_version=1,
    scale_to_zero=True,
    environment_vars={"VS_INDEX_NAME": vs_index_table_name}
)

# Wait for the Review App and deployed model to be ready
w = WorkspaceClient()
print("\nWaiting for endpoint to deploy.  This can take 15 - 20 minutes.", end="")

while ((w.serving_endpoints.get(deployment_info.endpoint_name).state.ready == EndpointStateReady.NOT_READY) or (w.serving_endpoints.get(deployment_info.endpoint_name).state.config_update == EndpointStateConfigUpdate.IN_PROGRESS)):
    print(".", end="")
    time.sleep(30)

print("\nThe endpoint is ready!", end="")

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Collect Human Feedback via Review App
# MAGIC
# MAGIC The Databricks Review App stages the LLM in an environment where expert stakeholders can engage with it, allowing for conversations, questions, and more. This setup enables the collection of valuable feedback on your application, ensuring the quality and safety of its responses.
# MAGIC
# MAGIC Stakeholders can interact with the application bot and provide feedback on these interactions. They can also offer feedback on historical logs, curated traces, or agent outputs.

# COMMAND ----------

print(f"Endpoint URL    : {deployment_info.endpoint_url}")
print(f"Review App URL  : {deployment_info.review_app_url}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC In this demo, you deployed the registered model using the Agent Framework, interacted with the deployed model through the Review App, and learned how the Review App can be used to collect human feedback for further analysis and model improvement.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
