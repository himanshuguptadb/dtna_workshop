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
# MAGIC # Tracking and Managing Models with MLflow
# MAGIC
# MAGIC In this demo, we will explore the model development lifecycle using MLflow. You’ll train a model, log artifacts, metrics, and parameters using MLflow, and then register the model in Unity Catalog for production readiness.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC - Train and log models using MLflow
# MAGIC - Track experiments and view runs using MLflow UI
# MAGIC - Register a model in Unity Catalog
# MAGIC - Use model version aliases like `staging` and `dev`

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

# MAGIC %run ../Includes/Classroom-Setup-mlflow

# COMMAND ----------

# MAGIC %md
# MAGIC Go over to the Catalog Explorer and see 2 new tables created:
# MAGIC 1. Table: `wine_quality_table`
# MAGIC 1. Table: `wine_quality_features`
# MAGIC
# MAGIC Note that the second table corresponds to what we created in the first demo, `01 - EDA and Feature Engineering`.

# COMMAND ----------

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### Exploring Tables in the Workspace
# MAGIC
# MAGIC After the classroom setup, two new tables and a model have been created in your workspace. To confirm their presence, you can use a SQL cell to list all available tables in your current schema.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- List all tables in the current schema
# MAGIC SHOW TABLES

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: Data Preparation for MLflow
# MAGIC
# MAGIC For this first part, we will read in a customer table, create a feature table, and register that feature table to Databricks Feature Store. This is all performed in the background and was covered in `01 - EDA and Feature Engineering`. Next, we will separate out our features from the target variable and perform a train-test split. 
# MAGIC
# MAGIC Note: We are working with a Pandas DataFrame called `training_df`.

# COMMAND ----------

# Load the feature table
training_df = spark.read.format('delta').table('wine_quality_features').toPandas()

# COMMAND ----------

# Define the mapping
mapping = {'Low': 0.0, 'Average': 1.0, 'High': 2.0}

# Apply the mapping to the 'pHCategory' column
training_df['pHCategory'] = training_df['pHCategory'].map(mapping)
# Use the training dataset to store variables X, the features, and y, the target variable. 
X = training_df.drop(columns = ["quality"])
y = training_df["quality"]



# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# COMMAND ----------

display(training_df)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Part 2: Training And Model Tracking/Management With MLflow
# MAGIC
# MAGIC Now that we have our training set ready to go, the next step is to train a model using the `sklearn` library. We will build a random forest classification model, tracking the F1-score for a single run. We will initiate the tracking before creating the model using `mlflow.start_run()` as the context manager. Within this manager we will:
# MAGIC
# MAGIC 1. Initialize the random forest classifier
# MAGIC 2. Fit the model
# MAGIC Make a prediction using our test set
# MAGIC 3. Log the F1-score metric as `test_f1`
# MAGIC 4. Capture the artifacts for model tracking and management using the flavor `mlflow.sklearn`. *Flavor* in this context simply means that MLflow will package our scikit-learn model in a consistent and standardized way. If we wished to use a different ML library, we would use a different *flavor*.
# MAGIC
# MAGIC Finally, we will register the model to Unity Catalog. Note, Databricks does not recommend registering your model at the Workspace level. Recall that we did this using the UI in the previous lab `02 - Experimentation with Mosaic AI AutoML`.
# MAGIC
# MAGIC

# COMMAND ----------

import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# set the path for mlflow experiment
mlflow.set_experiment(f"/Users/{DA.username}/get-started-with-ml-flow-experiment")

with mlflow.start_run(run_name = 'get-started-with-ml-flow-run') as run:  
    # Initialize the Random Forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

    # Fit the model on the training data
    rf_classifier.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = rf_classifier.predict(X_test)

    # Enable automatic logging of input samples, metrics, parameters, and models
    mlflow.sklearn.autolog(
        log_input_examples = True,
        silent = True
    )
    # Calculate F1 score with 'macro' averaging for multiclass
    mlflow.log_metric("test_f1", f1_score(y_test, y_pred, average='macro'))
    # mlflow.log_metric("test_f1", f1_score(y_test, y_pred))
        
    mlflow.sklearn.log_model(
        rf_classifier,
        artifact_path = "model-artifacts", 
        input_example=X_train[:3],
        signature=infer_signature(X_train, y_train)
    )

    model_uri = f"runs:/{run.info.run_id}/model-artifacts"

# COMMAND ----------

# Modify the registry uri to point to Unity Catalog
mlflow.set_registry_uri("databricks-uc")

# Define the model name 
model_name = f"{DA.catalog_name}.{DA.schema_name}.my_model_{DA.unique_name('-')}"

# Register the model in the model registry
registered_model = mlflow.register_model(model_uri=model_uri, name=model_name)

# COMMAND ----------

# MAGIC %md
# MAGIC Notice that you will now have an additional version under your model. Navigate to your model in Catalog explorer. You will find version 1 (created during the classroom setup with alias **staging**) and version 2, which you must created.

# COMMAND ----------

from mlflow.tracking.client import MlflowClient

# Initialize an MLflow Client
client = MlflowClient()

# Assign a "dev" alias to model version 1
client.set_registered_model_alias(
    name= registered_model.name,  # The registered model name
    alias="dev",  # The alias representing the dev environment
    version=registered_model.version  # The version of the model you want to move to "dev"
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusions And Next Steps
# MAGIC
# MAGIC In this demo, we covered how to track, manage, and stage models using **MLflow** on Databricks. In the next notebook, you'll explore **Mosaic AI AutoML**, which abstracts many of these steps into a no-code/low-code UI-driven workflow. This will help you compare the manual MLflow approach with the AutoML pipeline, and understand how MLflow operates under the hood of AutoML.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
