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
# MAGIC
# MAGIC # Getting Started with Mosaic AI Model Serving
# MAGIC
# MAGIC In this lesson, we will focus on how to serve a registered model using **Mosaic AI Model Serving** for real-time inferencing. We’ll also introduce **Databricks Workflows** as a way to automate ML pipelines.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC By the end of this demo, you will be able to:
# MAGIC
# MAGIC 1. **Serve your model with Mosaic AI Model Serving**
# MAGIC     - Use the UI to serve your model.
# MAGIC     - Query the endpoint using the UI.
# MAGIC     - Explore the metrics and logs using the built-in dashboard.
# MAGIC
# MAGIC 2. **Introduction to ML With Workflows:**
# MAGIC     - Use the UI to demonstrate notebook automation for ML tasks via Databricks Workflows.

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
# MAGIC
# MAGIC ## Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC * To run this notebook, you need to use one of the following Databricks runtime(s): **16.4.x-cpu-ml-scala2.12**

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC To get into the lesson, we first need to build some data assets and define configuration variables required for this demonstration.
# MAGIC
# MAGIC This Model Serving Endpoint will be available to everyone and deployed once. Once it is created, you will see the message `"Endpoint 'firstName-lastName-endpoint' already exists."` when trying to create it again. This is to limit resource deployment within this workspace. The first creation will take between 5 and 10 minutes.
# MAGIC
# MAGIC **Do not delete or modify this endpoint in any way.**  
# MAGIC We will cover how to create the model serving endpoint later in this demo.
# MAGIC

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-Model_Serving

# COMMAND ----------

# MAGIC %md
# MAGIC Go over to the Catalog Explorer and see 2 new tables and two model has been created. Additionally, you either created a model serving endpoint or one of the output from the cell above indicates the model serving endpoint already exists. 
# MAGIC 1. Table: `wine_quality_table`
# MAGIC 1. Table: `wine_quality_features`
# MAGIC 1. Model: `my_model_<schema_name>`, 
# MAGIC 1. Model: `m02_prediction_base_model`
# MAGIC 1. Model Serving Endpoint: `firstName-lastName-endpoint`
# MAGIC
# MAGIC Note that the second table corresponds to what we created in the first demo, `01 - EDA and Feature Engineering`.

# COMMAND ----------

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Note🚨 : Below instructions are only for demonstration purposes. Please do not provision an endpoint. It is already created during the workspace setup.**

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Part 1: Mosaic AI Model Serving
# MAGIC
# MAGIC **Setting Up Model Serving**
# MAGIC
# MAGIC We can create Model Serving endpoints with the Databricks Machine Learning API or the Databricks Machine Learning UI. An endpoint can serve any registered Python MLflow model in the **Model Registry**.
# MAGIC
# MAGIC In order to keep it simple, in this demo, we are going to use the Model Serving UI for creating, managing and using the Model Serving endpoints. We can create model serving endpoints with the **"Serving"** page UI or directly from registered **"Models"** page.  
# MAGIC
# MAGIC Let's go through the steps of creating a model serving endpoint in Models page. **You will not actually create the endpoint.**
# MAGIC
# MAGIC - Go to **Models**. 
# MAGIC
# MAGIC - Select **Unity Catalog** at the top and select **Owned by me** as well.
# MAGIC
# MAGIC - Select the model you want to serve under the **Name** column. Notice this will take you to the Catalog menu. 
# MAGIC
# MAGIC - Click the **Serve this model** button on the top right. This will take you to the **Serving endpoints** screen.
# MAGIC
# MAGIC - Next in **General**, enter in a name of the form **firstName-lastName-endpoint**.
# MAGIC
# MAGIC - There are several configurations under **Served entities** that we will not discuss here. Leave **Entity**, **Compute type** and **Compute scale-out** to default values.You can select **Scale to zero** for this lesson as well. We will be deleting the endpoint at the end of this lesson, so this doesn't matter too much for our purposes. 
# MAGIC
# MAGIC - **Do not click Create** at the bottom right. The above instructions are only for demonstration purposes. **Do not provision an endpoint.**
# MAGIC
# MAGIC     - If you happen to accidentally create an endpoint, you can navigate to the left side bar and click on **Serving**. Then click on the model you began provisioning and click on the 3 vertical dots at the top right. Select **Delete**. Again, **Do not provision an endpoint.**
# MAGIC
# MAGIC - If you do click create, you will be met with an error saying "Endpoint with name 'firstName_lastName-endpoint' already exists." This is because we already setup this endpoint during the setup to this course. **Do not provision an endpoint by changing the name.**
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Model Serving Endpoint with Python
# MAGIC
# MAGIC **Note**:  We will not be creating a new endpoint in this **demonstration**. However, the code implementation is shown below.

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC
# MAGIC from mlflow.deployments import get_deploy_client
# MAGIC
# MAGIC client = get_deploy_client("databricks")
# MAGIC endpoint_name = f"{DA.username}-model"
# MAGIC endpoint_name = endpoint_name.replace("@databricks.com", "").replace('.', '-')
# MAGIC
# MAGIC # Check if the endpoint already exists
# MAGIC try:
# MAGIC     # Attempt to get the endpoint
# MAGIC     existing_endpoint = client.get_endpoint(endpoint_name)
# MAGIC     print(f"Endpoint '{endpoint_name}' already exists.")
# MAGIC except Exception as e:
# MAGIC     # If not found, create the endpoint
# MAGIC     if "RESOURCE_DOES_NOT_EXIST" in str(e):
# MAGIC         print(f"Creating a new endpoint: {endpoint_name}")
# MAGIC         endpoint = client.create_endpoint(
# MAGIC             name=endpoint_name,
# MAGIC             config={
# MAGIC                 "served_entities": [
# MAGIC                     {
# MAGIC                         "name": "my-model",
# MAGIC                         "entity_name": model_name,
# MAGIC                         "entity_version": "1",
# MAGIC                         "workload_size": "Small",
# MAGIC                         "scale_to_zero_enabled": True
# MAGIC                     }
# MAGIC                 ],
# MAGIC                 "traffic_config": {
# MAGIC                     "routes": [
# MAGIC                         {
# MAGIC                             "served_model_name": "my-model",
# MAGIC                             "traffic_percentage": 100
# MAGIC                         }
# MAGIC                     ]
# MAGIC                 }
# MAGIC             }
# MAGIC         )
# MAGIC     else:
# MAGIC         print(f"An error occurred: {e}")
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query Serving Endpoint
# MAGIC
# MAGIC Let's use the deployed model for real-time inference. Here’s a step-by-step guide for querying an endpoint in Databricks Model Serving:
# MAGIC
# MAGIC - Go to the **Serving** endpoints page and select the endpoint you want to query.
# MAGIC
# MAGIC - Click **Use** button the top right corner.
# MAGIC
# MAGIC - There are 4 methods for querying an endpoint; **browser**, **CURL**, **Python**, and **SQL**. For now, let's use the easiest method; querying right in the **browser** window. In this method, we need to provide the input parameters in JSON format. Since we used `mlflow.sklearn.autolog()` with `log_input_examples = True`, we registered an example with MLflow, which appear automatically when selecting **browser**.
# MAGIC
# MAGIC - Click **Send request**.
# MAGIC
# MAGIC - **Response** field on the right panel will show the result of the inference.

# COMMAND ----------

# DBTITLE 1,Cell 14
import mlflow
from mlflow import MlflowClient

model_name = f"dbacademy.himanshu_gupta.my_model_{DA.schema_name}"

# Get the latest model version
client = MlflowClient()
versions = client.search_model_versions(f"name='{model_name}'")
latest_version = max([int(v.version) for v in versions])

model_uri = f"models:/{model_name}/{latest_version}"
model = mlflow.pyfunc.load_model(model_uri)

print(f"Using model version: {latest_version}")

# Example input as a pandas DataFrame
import pandas as pd

# Multiple wine samples with varying characteristics
input_data = pd.DataFrame([
    {
        "wine_id": 0,
        "fixed_acidity": 4.6,
        "volatile_acidity": 0.52,
        "citric_acid": 0.15,
        "pH": 3.9,
        "sulphates": 0.56,
        "alcohol": 13.1,
        "pHCategory": 4.0
    },
    {
        "wine_id": 1,
        "fixed_acidity": 4.7,
        "volatile_acidity": 0.6,
        "citric_acid": 0.17,
        "pH": 3.85,
        "sulphates": 0.6,
        "alcohol": 12.9,
        "pHCategory": 6.0
    },
    {
        "wine_id": 2,
        "fixed_acidity": 5.0,
        "volatile_acidity": 1.02,
        "citric_acid": 0.04,
        "pH": 3.75,
        "sulphates": 0.48,
        "alcohol": 10.5,
        "pHCategory": 4.0
    },
    {
        "wine_id": 3,
        "fixed_acidity": 5.0,
        "volatile_acidity": 1.04,
        "citric_acid": 0.24,
        "pH": 3.74,
        "sulphates": 0.62,
        "alcohol": 11.5,
        "pHCategory": 5.0
    },
    {
        "wine_id": 4,
        "fixed_acidity": 5.1,
        "volatile_acidity": 0.47,
        "citric_acid": 0.02,
        "pH": 3.9,
        "sulphates": 0.62,
        "alcohol": 12.8,
        "pHCategory": 6.0
    }
])

predictions = model.predict(input_data)
display(pd.DataFrame(predictions, columns=["prediction"]))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: ML With Workflows (Optional)
# MAGIC
# MAGIC ### Creating a Job
# MAGIC
# MAGIC Now, let's create a workflow job to run this notebook:
# MAGIC
# MAGIC 1. Start by navigating to **Jobs & Pipelines** on the left sidebar.
# MAGIC
# MAGIC 2. You have 2 options to proceed:
# MAGIC
# MAGIC     Option 1: Navigate to the **Job Runs** tab, then click **Create Job** at the top-right corner.
# MAGIC
# MAGIC     Option 2: In the **Jobs and Pipelines** section, click the **Create** dropdown at the top-right corner, and select **Job** from the options.
# MAGIC
# MAGIC **Note:** Please make sure Lakeflow Pipelines Editor is turned **ON**.
# MAGIC
# MAGIC 3. Click on **Notebook**.   
# MAGIC
# MAGIC 3. In the presented menu, enter a name under **Task Name**. For example, you can use **test_task_name**.
# MAGIC
# MAGIC 4. Under **Type**, ensure that **Notebook** is selected. Also, make sure **Workspace** is selected under **Source**. Both should be selected by default.
# MAGIC
# MAGIC 5. Next, we will attach this notebook to the job. Go to **Path**. Click the drop-down menu. You will be presented with a menu that will allow you to navigate to this notebook. By default, you will already be in your home workspace. Click the source folder (there will only be a single option listed other than **Trash**). Select `M02 - Databricks for Machine Learning` and then select `04 - Getting Started with Mosaic AI Model Serving`. Click **Confirm** at the bottom right of the **Select Notebook** menu. 
# MAGIC
# MAGIC 6. Under **Compute**, you'll see **Serverless** is automatically selected.
# MAGIC Use the drop-down menu to select your existing All-Purpose **cluster**.
# MAGIC
# MAGIC 7. You’ll see additional options, such as **dependent libraries**, **parameters**, **notifications**, **retries**, and **Metric threshold**. You can leave these options unpopulated for this lesson. 
# MAGIC
# MAGIC 8. Click **Create Task**. A message will appear at the top right indicating your task was successfully created.
# MAGIC
# MAGIC 9. In the right menu, there are various options. For example, you can add tags, set job parameters, and configure schedules for runs. We'll leave these alone for this lesson.
# MAGIC
# MAGIC 10. Finally, to give the job a name, double-click the title at the top left and enter an appropriate name. For example, `Workflow1`.
# MAGIC
# MAGIC 11. When you are ready to run the job, click **Run Now** at the top right. A note will appear at the top right indicating a run has been initiated. Note that due to the clean-up in the next cell, your data assets will be missing when inspecting your catalog after the job finishes. 
# MAGIC
# MAGIC ### Inspect Your Run
# MAGIC
# MAGIC After your job completes its run, you can inspect it:
# MAGIC
# MAGIC 1. Select **Jobs & Pipelines** again on the sidebar menu. 
# MAGIC
# MAGIC 1. Click on the name of the job you just created. 
# MAGIC
# MAGIC 1. There are a few ways to view the notebook you just ran. You can do any of the following and it will take you to the same location:
# MAGIC     - Click on **go to the latest successful run**.
# MAGIC     - Click on the date under **Start time**.
# MAGIC     - Click on the green bar (meaning a successful run) displayed within the diagram. If the bar is red, that means your job failed, but you can still inspect the notebook that ran. This option will also display the workflow configuration you setup previously. 
# MAGIC
# MAGIC 1. This will take you to a static copy of the notebook. You cannot edit it, but you can view the outputs of each cell. Confirm that all cells have run successfully. 
# MAGIC
# MAGIC Of course, this is a simple example of creating a job with a single notebook. In practice, we use the various options mentioned earlier to tie together complex pipelines.

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusions And Next Steps
# MAGIC
# MAGIC In this demo, you learned how to use **Mosaic AI Model Serving** for real-time inference with a registered model. You also explored **Databricks Workflows** as a way to schedule and automate ML jobs.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
