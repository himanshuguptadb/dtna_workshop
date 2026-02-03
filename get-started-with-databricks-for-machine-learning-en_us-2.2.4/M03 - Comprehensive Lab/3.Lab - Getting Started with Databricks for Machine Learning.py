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
# MAGIC # 3.Lab - Getting Started with Databricks for Machine Learning
# MAGIC
# MAGIC In this lab, we will construct a comprehensive ML model pipeline using Databricks. Initially, we will train and monitor our model using mlflow. Subsequently, we will register the model and advance it to the next stage. In the latter part of the lab, we will utilize Model Serving to deploy the registered model. Following deployment, we will interact with the model via a REST endpoint and examine its behavior through an integrated monitoring dashboard.
# MAGIC

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
# MAGIC
# MAGIC ## Lab Setup
# MAGIC
# MAGIC To ensure a smooth experience, follow these initial steps:
# MAGIC
# MAGIC 1. Run the provided classroom setup script. This script will establish necessary configuration variables tailored to each user. Execute the following code cell:

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-Lab

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC **Other Conventions:**
# MAGIC
# MAGIC Throughout this lab, we'll make use of the object `DA`, which provides critical variables. Execute the code block below to see various variables that will be used in this notebook:
# MAGIC

# COMMAND ----------

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

# COMMAND ----------

# MAGIC %md
# MAGIC Let's set our catalog and schema to variables `my_catalog` and `my_schema` since we'll be using them in this demo.

# COMMAND ----------

my_catalog = DA.catalog_name
my_schema = DA.schema_name

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Data Ingestion
# MAGIC  - The first step in this lab is to ingest data from .csv files and save them as delta tables. Navigate to the Catalog explorer and locate the datasets under shared and find `dbacademy_airbnb`. Expand `v01` and `locate airbnb-cleaned-mlflow.csv` located in the volume `sf-listings`. 
# MAGIC  - Second, we grab a few relevant features to help train our model to predict the target variable for this dataset, `price`.

# COMMAND ----------

## Copy and paste the location of the airbnb dataset
file_path = '<FILL_IN>'

# COMMAND ----------

# MAGIC %skip
# MAGIC file_path = '/Volumes/dbacademy_airbnb/v01/sf-listings/airbnb-cleaned-mlflow.csv'

# COMMAND ----------

## Read in the csv file and store it in Unity Catalog within the catalog and schema shown in cell 7. 
## Name your delta table "airbnb_lab"
my_table = <FILL_IN>
df = spark.read.format(<FILL_IN>).option("header", "true").load(<FILL_IN>)

# COMMAND ----------

# MAGIC %skip
# MAGIC my_table = "airbnb_lab"
# MAGIC df = spark.read.format("csv").option("header", "true").load(file_path)
# MAGIC
# MAGIC display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC Let's preprocess this dataset since the schema shows all variables being of time `string`.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import FloatType, IntegerType, StringType

## Specify columns that should be treated as categorical (e.g., integers in categorical context)
categorical_columns = ['neighbourhood_cleansed', 'zipcode', 'property_type', 'room_type', 'bed_type']
for col in categorical_columns:
    df = df.withColumn(col, df[col].cast(StringType()))

## Specify columns that should remain as floats for machine learning
numerical_columns = ['host_total_listings_count', 'latitude', 'longitude', 'accommodates', 'bathrooms', 
                 'bedrooms', 'beds', 'minimum_nights', 'number_of_reviews', 'review_scores_rating',
                 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin',
                 'review_scores_communication', 'review_scores_location', 'review_scores_value', 'price']
for col in numerical_columns:
    df = df.withColumn(col, df[col].cast(FloatType()))

df = df.withColumn("airbnb_id", F.monotonically_increasing_id()).select(['airbnb_id'] + numerical_columns + categorical_columns)

## Check the schema to confirm data type changes
df.printSchema()

# COMMAND ----------

df.write.format('delta').mode('overwrite').saveAsTable('airbnb_lab')

# COMMAND ----------

# MAGIC %md
# MAGIC # Feature Engineering

# COMMAND ----------

# MAGIC %md
# MAGIC Next, using PySpark, create a DataFrame called `feature_df` that is the feature table. Recall that the feature table must contain a primary key and does not contain the target variable, which is `price` in our case.

# COMMAND ----------

feature_df = df.select(<FILL_IN>)

## Find rooms with a score of at least 6.0 and 80 reviews
feature_df = feature_df.filter((<FILL_IN>) & (<FILL_IN>))
display(feature_df)

# COMMAND ----------

# MAGIC %skip
# MAGIC feature_df = df.select(['airbnb_id'] + numerical_columns)
# MAGIC
# MAGIC ## Find rooms with a score of at least 6.0 and 80 reviews
# MAGIC feature_df = feature_df.filter((df.review_scores_rating >= 6.0) & (df.number_of_reviews >= 80))
# MAGIC display(feature_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Write to Databricks Feature Store. Remember, we do not include our target variable.

# COMMAND ----------

## Write feature_df to Databricks Feature Store. 
from databricks.feature_store import FeatureStoreClient

fs = FeatureStoreClient()

feature_df = feature_df.drop(<FILL_IN>)

fs.create_table(
    name="airbnb_features",
    primary_keys = <FILL_IN>, 
    df = <FILL_IN>,
    description = "This is the airbnb feature table",
    tags = {"source": "bronze", "format": "delta"}
    )

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Write feature_df to Databricks Feature Store.
# MAGIC from databricks.feature_store import FeatureStoreClient
# MAGIC
# MAGIC fs = FeatureStoreClient()
# MAGIC
# MAGIC feature_df = feature_df.drop("price")
# MAGIC
# MAGIC fs.create_table(
# MAGIC     name="airbnb_features",
# MAGIC     primary_keys = ['airbnb_id'], 
# MAGIC     df = feature_df,
# MAGIC     description = "This is the airbnb feature table",
# MAGIC     tags = {"source": "bronze", "format": "delta"}
# MAGIC     )

# COMMAND ----------

# MAGIC %md
# MAGIC # Train a Model
# MAGIC To summarize what you have accomplished so far:
# MAGIC 1. You have created a table that is a snapshot of the original dataset (Airbnb csv file) called `airbnb_lab`.
# MAGIC 1. You have created a feature table and stored it in Databricks Feature Store called `airbnb_features`.
# MAGIC
# MAGIC Next, we will simulate the process of reading in these Delta tables and training a model. We will train a machine learning model and register it to Unity Catalog.

# COMMAND ----------

## Read in the feature table airbnb_features from Unity Catalog using PySpark and store it as training_df
prediction_df = spark.read.format('delta').table(<FILL_IN>).select(<FILL_IN>)
features_df = spark.read.format('delta').table(<FILL_IN>)  

## Join these two dataframes on airbnb_id
training_df = prediction_df.join(<FILL_IN>, on='airbnb_id').toPandas()

## Perform train-test split
X = training_df.drop(columns = [<FILL_IN>])
y = training_df[<FILL_IN>]

X_train, X_test, y_train, y_test = train_test_split(<FILL_IN>, <FILL_IN>, test_size=0.2, random_state=42)

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Read in the feature table airbnb_features from Unity Catalog using PySpark and store it as training_df
# MAGIC prediction_df = spark.read.format('delta').table('airbnb_lab').select('airbnb_id','price')
# MAGIC features_df = spark.read.format('delta').table('airbnb_features')
# MAGIC
# MAGIC ## Join these two dataframes on airbnb_id
# MAGIC training_df = prediction_df.join(features_df, on='airbnb_id').drop('airbnb_id')
# MAGIC training_pdf = training_df.toPandas()
# MAGIC
# MAGIC ## Perform train-test split
# MAGIC X = training_pdf.drop(columns = ['price'])
# MAGIC y = training_pdf['price']
# MAGIC
# MAGIC X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Model Tracking and Management with MLflow
# MAGIC
# MAGIC Next, you will use MLflow to track the training of your model.

# COMMAND ----------

## Set the path for mlflow experiment
mlflow.set_experiment(f"/Users/{DA.username}/<FILL_IN>")

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Set the path for mlflow experiment
# MAGIC mlflow.set_experiment(f"/Users/{DA.username}/model-serving-experiment")

# COMMAND ----------

## Start the MLflow run
with mlflow.start_run(run_name=<FILL_IN>) as run:
    ## Initialize the Random Forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=<FILL_IN>, random_state=42)

    ## Fit the model on the training data
    rf_classifier.fit(<FILL_IN>, <FILL_IN>)

    ## Make predictions on the test data
    y_pred = rf_classifier.predict(<FILL_IN>)

    ## Enable automatic logging of input samples, metrics, parameters, and models
    mlflow.sklearn.autolog(log_input_examples=<FILL_IN>, silent=True)
    ## Calculate F1 score with 'macro' averaging for multiclass
    mlflow.log_metric("test_f1", f1_score(<FILL_IN>, <FILL_IN>, average="macro"))
    ## mlflow.log_metric("test_f1", f1_score(y_test, y_pred))

    mlflow.sklearn.log_model(
        rf_classifier,
        artifact_path="model-artifacts",
        input_example=X_train[:3],
        signature=infer_signature(<FILL_IN>, <FILL_IN>),
    )

    model_uri = f"runs:/{run.info.run_id}/model-artifacts"

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Start the MLflow run
# MAGIC with mlflow.start_run(run_name="model-serving-run") as run:
# MAGIC     ## Initialize the Random Forest classifier
# MAGIC     rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
# MAGIC
# MAGIC     ## Fit the model on the training data
# MAGIC     rf_classifier.fit(X_train, y_train)
# MAGIC
# MAGIC     ## Make predictions on the test data
# MAGIC     y_pred = rf_classifier.predict(X_test)
# MAGIC
# MAGIC     ## Enable automatic logging of input samples, metrics, parameters, and models
# MAGIC     mlflow.sklearn.autolog(log_input_examples=True, silent=True)
# MAGIC     ## Calculate F1 score with 'macro' averaging for multiclass
# MAGIC     mlflow.log_metric("test_f1", f1_score(y_test, y_pred, average="macro"))
# MAGIC     ## mlflow.log_metric("test_f1", f1_score(y_test, y_pred))
# MAGIC
# MAGIC     mlflow.sklearn.log_model(
# MAGIC         rf_classifier,
# MAGIC         artifact_path="model-artifacts",
# MAGIC         input_example=X_train[:3],
# MAGIC         signature=infer_signature(X_train, y_train),
# MAGIC     )
# MAGIC
# MAGIC     model_uri = f"runs:/{run.info.run_id}/model-artifacts"

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Register the Model
# MAGIC
# MAGIC Now, let's register the trained model in the model registry:
# MAGIC
# MAGIC 1. Use the logged model from the previous step.
# MAGIC 2. Provide a name and description for the model.
# MAGIC 3. Register the model to Unity Catalog.

# COMMAND ----------

## Modify the registry uri to point to Unity Catalog
mlflow.set_registry_uri("databricks-uc")

model_name = f"gs_db_ml_LAB_{DA.unique_name('-')}"

## Register the model in the model registry
registered_model = <FILL_IN>

# COMMAND ----------

# MAGIC %skip
# MAGIC ## Modify the registry uri to point to Unity Catalog
# MAGIC mlflow.set_registry_uri("databricks-uc")
# MAGIC
# MAGIC model_name = f"gs_db_ml_LAB_{DA.unique_name('-')}"
# MAGIC
# MAGIC ## Register the model in the model registry
# MAGIC registered_model = mlflow.register_model(model_uri=model_uri, name=model_name)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Manage Model Stages
# MAGIC
# MAGIC As the model is registered into Model Registry, we can manage its stage using the UI or the API. In this demo, we will use the API to transition registered model to `Staging` stage.

# COMMAND ----------

from mlflow.tracking.client import MlflowClient
client = MlflowClient()

## Transition the model to the "lab-staging" stage
client.<FILL_IN>(
    name = <FILL_IN>,
    version = <FILL_IN>,
    stage = <FILL_IN>
)

# COMMAND ----------

# MAGIC %skip
# MAGIC from mlflow.tracking.client import MlflowClient
# MAGIC
# MAGIC ## Initialize an MLflow Client
# MAGIC client = MlflowClient()
# MAGIC
# MAGIC ## Assign a "staging" alias to model version 1
# MAGIC client.set_registered_model_alias(
# MAGIC     name= registered_model.name,  # The registered model name
# MAGIC     alias="lab-staging",  # The alias representing the staging environment
# MAGIC     version=registered_model.version  # The version of the model you want to move to "staging"
# MAGIC )

# COMMAND ----------

# MAGIC %md
# MAGIC **Note🚨 : Below instructions are only for demonstration purposes. Please do not provision an endpoint using the UI. See the instructions for querying in the section titled Query Serving Endpoint in the event that your model serving endpoint no longer exists.**

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Part 3: Mosaic AI Model Serving
# MAGIC
# MAGIC **Setting Up Model Serving**
# MAGIC
# MAGIC We can create Model Serving endpoints with the Databricks Machine Learning API or the Databricks Machine Learning UI. An endpoint can serve any registered Python MLflow model in the **Model Registry**.
# MAGIC
# MAGIC In order to keep it simple, in this lab, we are going to use the Model Serving UI for creating, managing and using the Model Serving endpoints. We can create model serving endpoints with the **"Serving"** page UI or directly from registered **"Models"** page.  
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
# MAGIC - Next in **General**, enter in a name of the form **firstName_lastName-endpoint**.
# MAGIC
# MAGIC - There are several configurations under **Served entities** that we will not discuss here. Leave **Entity**, **Compute type** and **Compute scale-out** to default values. You can select **Scale to zero** for this lesson as well. We will be deleting the endpoint at the end of this lesson, so this doesn't matter too much for our purposes. 
# MAGIC
# MAGIC - **Do not click Create** at the bottom right. The above instructions are only for demonstration purposes. **Do not provision an endpoint.**
# MAGIC
# MAGIC     - If you happen to accidentally create an endpoint, you can navigate to the left side bar and click on **Serving**. Then click on the model you began provisioning and click on the 3 vertical dots at the top right. Select **Delete**. Again, **Do not provision an endpoint.**
# MAGIC
# MAGIC

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
# MAGIC - There are 4 methods for querying an endpoint; **browser**, **CURL**, **Python**, and **SQL**. For now, let's use the easiest method; querying right in the **browser** window. In this method, we need to provide the input parameters in JSON format. Recall that we registered an example with MLflow, which appears automatically when selecting **browser**.
# MAGIC
# MAGIC - Click **Send request**.
# MAGIC
# MAGIC - **Response** field on the right panel will show the result of the inference.
# MAGIC
# MAGIC
# MAGIC **FAQ**
# MAGIC 1. _My endpoint is gone!_ Don't panic if your endpoint is missing. Run the following two cells to deploy a new one.
# MAGIC 1. _I want to deploy the model I created in this notebook._ It may be the case that you decided to stay in this workspace after going through demonstration 3. You can deploy and inference the model created in this notebook by ending your Vocareum lab environment, joining as a new user, and go through the lab once again. The cell containing the line `DA.create_model_serving_endpoint(model_version=model_version)` checks to see if the endpoint exists with a previous model and it will serve the model created here if no such endpoint exists. Please make sure you make a copy of your code since exiting the lab environment will erase your work.

# COMMAND ----------

model_name = registered_model.name
model_version = registered_model.version
print(f"Model name: {model_name}")
print(f"Model version: {model_version}")

# COMMAND ----------

DA.create_model_serving_endpoint(model_version=model_version)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lab, we explored the full potential of Databricks Data Intelligence Platform for machine learning tasks. From data ingestion to model deployment, we covered essential steps such as data preparation, model training, tracking, registration, and serving. By utilizing MLflow for model tracking and management, and Model Serving for deployment, we demonstrated how Databricks offers a seamless Lakeflow Jobs for building and deploying ML models. Through this comprehensive lab, users can gain a solid understanding of Databricks capabilities for ML tasks and streamline their development process effectively.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
