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
# MAGIC # Experimentation with Mosaic AI AutoML
# MAGIC
# MAGIC In this demo, we will explore how **Mosaic AI AutoML** automates the process of model training, selection, and registration. 
# MAGIC
# MAGIC _In the previous demo, you manually tracked and registered models using MLflow. In this one, you’ll see how AutoML automates those steps while still leveraging the same tracking infrastructure._
# MAGIC
# MAGIC AutoML allows you to build, train, and evaluate models with minimal code. We will create an AutoML experiment, inspect the results, register the best model, and transition it to the **Staging** stage.
# MAGIC
# MAGIC **Learning Objectives**
# MAGIC
# MAGIC _By the end of this lesson, you will be able to:_
# MAGIC
# MAGIC 1. **Establish a baseline champion model with AutoML:**
# MAGIC     - Create an AutoML experiment using the Experiments UI.
# MAGIC     - (Optional) Create an AutoML experiment using the `databricks` Python library. 
# MAGIC     - Understand the various configuration options available in AutoML experiments.
# MAGIC 2. **Model and notebook inspection:**
# MAGIC     - Evaluate the results of an AutoML experiment and identify the champion model.
# MAGIC     - (Optional) Explore results using a notebook and open the generated code for the best run.
# MAGIC 3. **Register the champion model:**
# MAGIC     - Register the model within Unity Catalog.

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
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC To get into the lesson, we first need to build some data assets and define some configuration variables required for this demonstration. When running the following cell, the output is hidden so our space isn't cluttered. To view the details of the output, you can hover over the next cell and click the eye icon. 
# MAGIC
# MAGIC The cell after the setup, titled `View Setup Variables`, displays the various variables that were created. You can click the Catalog icon in the notebook space to the right to see that your catalog was created with no data.

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-AutoML

# COMMAND ----------

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Prepare Data
# MAGIC
# MAGIC We will use the same dataset from the previous demo (`wine_quality_table`) to maintain continuity. This dataset includes chemical properties like pH levels and alcohol content, used to predict wine quality.

# COMMAND ----------

spark.table('wine_quality_table').printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: Create and Run an AutoML Experiment
# MAGIC
# MAGIC Here we will discuss two methods for creating an AutomL experiment:
# MAGIC 1. Using the Databricks UI. 
# MAGIC 2. (Optional) Programmatically using the `databricks` Python library.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Create An AutoML Experiment With The UI
# MAGIC
# MAGIC Let's initiate an AutoML experiment to construct a baseline model for predicting wine quality. The target field for this prediction will be the `quality` field.
# MAGIC
# MAGIC Follow these step-by-step instructions to create an AutoML experiment:
# MAGIC
# MAGIC 1. Navigate to **Experiments** under **AI/ML** in the left sidebar menu.
# MAGIC
# MAGIC 1. Click on **Classification**.
# MAGIC
# MAGIC   ![automl-create-experiment-v1](../Includes/images/automl-create-experiment-v1.png)
# MAGIC
# MAGIC 1. Choose a cluster to execute the experiment.
# MAGIC
# MAGIC 1. To select the `wine_quality_table` table as the input training data, select `Browse` under `Input training dataset` and navigate to the catalog and the same database we've been using (see **Classroom Setup** in this notebook). 
# MAGIC
# MAGIC 1. Specify **`quality`** as the **Prediction target**.
# MAGIC
# MAGIC 1. Deselect the **wine_id** field as it's not needed as a feature.
# MAGIC
# MAGIC 1. In **Experiment name** you will see an automatically generated string. Append this string with your first and last name or some other unique identifier like  `<generated_name>-firstName_lastName`. If a message appears that indicates the name is taken, try a different set of string values to append to the experiment name. 
# MAGIC
# MAGIC 1. In the **Advanced Configuration** section, set the **Timeout** to **5 minutes**.
# MAGIC
# MAGIC 1. Click on **Start AutoML**. 
# MAGIC
# MAGIC **Optional Advanced Configuration:**
# MAGIC
# MAGIC - You have the flexibility to choose the **evaluation metric** and your preferred **training framework**.
# MAGIC
# MAGIC - If your dataset includes a timeseries field, you can define it when splitting the dataset.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### (Optional) Create An AutoML Experiment Within A Notebook
# MAGIC
# MAGIC We can Programmatically kickoff an AutoML experiment using the `databricks` Python library as well. After clicking **Run** on the following cell, you can go over to **Experiments** on the left menu bar and navigate to the experiment.

# COMMAND ----------

from databricks import automl
from datetime import datetime
# Define parameters for the classify function
table_name = "wine_quality_table" # The table containing our features and labels
target_col = "quality" # The variable we are trying to predict
exclude_cols = ["wine_id"] # Exclude the table column
timeout_minutes = 10  # The maximum time in minutes to run the experiment (minimum of 5 minutes)


# Run the AutoML experiment to generate the best classify model and generate the best run notebook
automl_run = automl.classify(
    dataset=spark.table(table_name), 
    target_col=target_col, 
    exclude_cols=exclude_cols, 
    timeout_minutes=timeout_minutes)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: Best Run Inspection
# MAGIC
# MAGIC Next, we will inspect the best run produced by AutoML:
# MAGIC
# MAGIC 1. Using the Databricks UI. 
# MAGIC 2. (Optional) Programmatically using the `databricks` Python library.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Best Run Inspection With The UI
# MAGIC
# MAGIC Once the experiment is finished, it's time to examine the best run:
# MAGIC
# MAGIC 1. Access the completed experiment in the **Experiments** section.
# MAGIC
# MAGIC 2. Identify the best model run by evaluating the displayed **metrics**. Alternatively, you can click on **View notebook for best model** to access the automatically generated notebook for the top-performing model.
# MAGIC
# MAGIC 3. Utilize the **Chart** tab to compare and contrast the various models generated during the experiment.
# MAGIC
# MAGIC > `You’ve seen these steps earlier in the MLflow demo, AutoML builds on the same infrastructure but streamlines the setup.`
# MAGIC
# MAGIC You can find all details for the run  on the experiment page. There are different columns such as the framework used (e.g., Scikit-Learn, XGBoost), evaluation metrics (e.g., Accuracy, F1 Score), and links to the corresponding notebooks for each model. This allows you to make informed decisions about selecting the best model for your specific use case.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### (Optional) Best Run Inspection Within A Notebook 
# MAGIC
# MAGIC Alternatively, we can approach the inspection programmatically. First, we will display all the experiments only we have created. Second, we will create Pandas DataFrame that contains F1-score information along with a visual to help pick the champion model. 
# MAGIC
# MAGIC **Notebooks for Other Experiment Trials in AutoML**
# MAGIC
# MAGIC For classification and regression experiments, AutoML generated notebooks for data exploration and the best trial in your experiment are automatically imported to your workspace. For all trials besides the best trial, the notebooks **are NOT created** automatically. If you need to use these notebooks, you can manually import them into your workspace with the **`automl.import_notebook`** Python API.

# COMMAND ----------

import mlflow

# Initialize MLflow client
client = mlflow.tracking.MlflowClient()

# List all experiments using search_experiments()
experiments = client.search_experiments()

# Loop through experiments and check if the username is part of the experiment name or artifact location
for experiment in experiments:
    if DA.username in experiment.name or DA.username in experiment.artifact_location:
        print(f"Experiment ID: {experiment.experiment_id}, \nName: {experiment.name}, \nArtifact Location: {experiment.artifact_location}\n")

# COMMAND ----------

# MAGIC %md
# MAGIC Let's grab only the latest experiment, assuming that's the run we want. You can modify this code to grab a specific experiment if needed.

# COMMAND ----------

for experiment in experiments:
    if DA.username in experiment.name or DA.username in experiment.artifact_location:
        latest_experiment_name = experiment.name
        break
print(f"Latest experiment name: {latest_experiment_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC Now that we have the name of our latest experiment, we can construct a Pandas DataFrame that grabs the F1-score for visual inspection.

# COMMAND ----------

import mlflow
import pandas as pd

# Step 1: Get the experiment by name
experiment = mlflow.get_experiment_by_name(latest_experiment_name)

# Initialize an empty list to store the data for the DataFrame
data = []

if experiment:
    experiment_id = experiment.experiment_id
    
    # Step 2: Retrieve all runs from the experiment
    runs = mlflow.search_runs(experiment_ids=experiment_id)
    
    # Step 3: Access the F1 scores for training, validation, and test data
    for _, run in runs.iterrows():
        run_id = run['run_id']
        
        # Fetch the run data
        run_data = mlflow.get_run(run_id)
        
        # Fetch F1 scores
        train_f1_score = run_data.data.metrics.get('training_f1_score', None)
        val_f1_score = run_data.data.metrics.get('val_f1_score', None)
        test_f1_score = run_data.data.metrics.get('test_f1_score', None)
        
        # Append the data for this run to the list
        data.append({
            'run_id': run_id,
            'train_f1_score': train_f1_score,
            'validation_f1_score': val_f1_score,
            'test_f1_score': test_f1_score
        })

    # Convert the list of data into a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Display or return the DataFrame
    display(df)
else:
    print(f"Experiment {experiment} not found.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Part 3: Register the Best Model Using the UI
# MAGIC
# MAGIC 1. If you have not already done so, navigate to **Experiments** on the left sidebar menu.
# MAGIC 1. Find the AutoML experiment you ran previously and click on the name. 
# MAGIC 1. Select the name of the top run in the table. Notice the sort widget says `test_f1_score` automatically, so the table prioritizes this metric be default. 
# MAGIC 1. Select **Register model** at the top right. 
# MAGIC 1. In the dialog box, you will be presented with two options: Workspace Model Registry and Unity Catalog. If you select to register the model at the workspace-level, you will need to simply enter in the name of the model. If you wish to use Unity Catalog, you will need to provide the model name in the format `<catalog_name>.<schema_name>.<model_name>`. Select **Unity Catalog** and enter **`M02_prediction_base_model`** as model name for the catalog and schema we've been working in. For example, `dbacademy.new_craw.M02_prediction_base_model` would be acceptable. 
# MAGIC 1. Finally, click the **Register** button to complete the registration process. You will see a message indicating the registration process has started. 
# MAGIC 1. Navigate to **Catalog**. After finding the catalog and schema where you saved your model, you will find your newly registered model either in the **Catalog Explorer** or by clicking on the schema and selecting the **Models** tab. 
# MAGIC
# MAGIC Your model is now registered and ready for inferencing. We will discuss how to query a model in the next lesson.

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusion And Next Steps
# MAGIC
# MAGIC In this demo, you learned how to utilize AutoML to quickly generate baseline models with minimal code, while still leveraging the same tracking and model management infrastructure powered by MLflow. 
# MAGIC
# MAGIC We also explored how to evaluate the best model, inspect its automatically generated notebook, and register the champion model for future use.
# MAGIC
# MAGIC In the next lesson, In the next lesson, you'll explore **Mosaic AI Model Serving**, where you will learn how to serve the models you’ve registered—whether through MLflow or AutoML, for real-time inference.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
