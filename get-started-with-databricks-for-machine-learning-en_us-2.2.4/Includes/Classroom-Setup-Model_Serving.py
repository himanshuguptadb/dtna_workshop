# Databricks notebook source
# This notebook creates a model serving endpoint based on tables and feature tabels created in Classroom-Setup-2.

# COMMAND ----------

# MAGIC %run ./_common

# COMMAND ----------

# %run ./Classroom-Setup-2

# COMMAND ----------

import warnings
warnings.filterwarnings("ignore")

import numpy as np
np.set_printoptions(precision=2)

import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)

# COMMAND ----------

import pandas as pd

from pyspark.sql import functions as F
from pyspark.sql.functions import col, when
from pyspark.sql.utils import AnalysisException
import pyspark.pandas as ps

import re

from databricks.feature_engineering import FeatureEngineeringClient

from sklearn.model_selection import train_test_split

# COMMAND ----------

@DBAcademyHelper.add_init
def create_demo_table(self):
    my_catalog = DA.catalog_name
    my_schema = DA.schema_name
    my_table = "wine_quality_table"
    spark.sql(f"USE CATALOG {my_catalog}")
    spark.sql(f"USE SCHEMA {my_schema}")

    # Load the original wine dataset
    data_path = f"{DA.paths.datasets.wine_quality}/data"
    try:
        spark.read.format("delta").table(data_path)
        print(
            f"Location where Delta table `wine_quality_table` already exists: {my_catalog}.{my_schema}.{my_table}"
        )

    except:
        df = (
            spark.read.format("delta")
            .load(data_path)
            .withColumn("wine_id", F.monotonically_increasing_id())
            .select(
                "wine_id",
                "fixed_acidity",
                "volatile_acidity",
                "citric_acid",
                "residual_sugar",
                "chlorides",
                "free_sulfur_dioxide",
                "total_sulfur_dioxide",
                "density",
                "pH",
                "sulphates",
                "alcohol",
                "quality",
            )
        )

        # Write to catalog and schema created with DA object
        df.write.format("delta").mode("overwrite").saveAsTable(my_table)

        print(
              f"Location of Delta table created: {my_catalog}.{my_schema}.{my_table}"
              )
        


@DBAcademyHelper.add_init
def create_feature_table(self):

    # Get catalog and schema information
    my_catalog = DA.catalog_name
    my_schema = DA.schema_name
    my_table = "wine_quality_table"
    feature_table_name = "wine_quality_features"

    fs = FeatureEngineeringClient()

    spark.sql(f"USE CATALOG {my_catalog}")
    spark.sql(f"USE SCHEMA {my_schema}")

    try:
        # Check if the feature table already exists
        existing_feature_table = fs.read_table(name=feature_table_name)
        #print(f"`{feature_table_name}` already exists in {my_catalog}.{my_schema}")

        # Check if the `quality` column exists in the current table
        if "quality" not in existing_feature_table.columns:
            #print(f"Adding missing column `quality` to `{feature_table_name}`...")

            # Read the source table and get the updated schema
            source_df = spark.read.format("delta").table(my_table)

            updated_df = existing_feature_table.join(
                source_df.select("wine_id", "quality"), on="wine_id", how="left"
            )

            # Update the feature table
            fs.write_table(
                name=feature_table_name,
                df=updated_df,
                mode="overwrite",
            )
        else:
            print(f"`{feature_table_name}` already exists in {my_catalog}.{my_schema}")

    except:
        print(f"Creating feature table `{feature_table_name}`...")

        # Read in the wine quality table
        df = spark.read.format("delta").table(my_table)

        # Calculate quantiles for pH to create a category column
        quantiles = df.approxQuantile("pH", [0.25, 0.75], 0.0)
        Q1, Q3 = quantiles

        # Add a `pHCategory` column
        df = df.withColumn(
            "pHCategory",
            when(col("pH") <= Q1, "Low")
            .when((col("pH") > Q1) & (col("pH") < Q3), "Average")
            .otherwise("High"),
        )

        # Select the required columns, including `quality`
        df = df.select(
            "wine_id",
            "fixed_acidity",
            "volatile_acidity",
            "citric_acid",
            "pH",
            "sulphates",
            "alcohol",
            "pHCategory",
            "quality",
        )

        # Create the feature table
        fs.create_table(
            name=feature_table_name,
            primary_keys=["wine_id"],
            df=df,
            description="This is a wine quality feature table",
            tags={"source": "bronze", "format": "delta"},
        )

        print(f"Feature table `{feature_table_name}` created successfully.")


@DBAcademyHelper.add_init
def create_model_serving_endpoint(self):
    # Import necessary libraries
    import mlflow
    import mlflow.sklearn
    from mlflow.models.signature import infer_signature
    from mlflow.deployments import get_deploy_client
    from mlflow.tracking.client import MlflowClient

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import f1_score

    import requests
    import json

    # Read in the feature table. If it doesn't exist, create it using DA.create_feature_table(). Be sure to convert it to a pandas DataFrame.
    try:
        feature_df = (
            spark.read.format("delta").table("wine_quality_features").toPandas()
        )
    except:
        DA.create_feature_table()
        feature_df = (
            spark.read.format("delta").table("wine_quality_features").toPandas()
        )

    # Define the mapping
    mapping = {"Low": 0.0, "Average": 1.0, "High": 2.0}

    # Apply the mapping to the 'pHCategory' column
    feature_df["pHCategory"] = feature_df["pHCategory"].map(mapping)
    # Use the training dataset to store variables X, the features, and y, the target variable.
    X = feature_df.drop(columns=["quality"])
    y = feature_df["quality"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Check to see if the model already exists.

    # Retrieve all active experiments
    experiments = mlflow.search_experiments()

    # Define the experiment name to check for
    target_experiment_name = f"/Users/{DA.username}/model-serving-experiment"

    # Check if the experiment exists
    experiment_exists = any(exp.name == target_experiment_name for exp in experiments)

    if experiment_exists:
        print(
            "The experiment 'model-serving-experiment' exists. Using this existing model for serving."
        )
        # Grab the model name
        model_name = (
            f"{DA.catalog_name}.{DA.schema_name}.my_model_{DA.unique_name('-')}"
        )
    else:
        print(
            "The experiment 'model-serving-experiment' does not exist. Creating a new model."
        )

        # Set the path for mlflow experiment
        mlflow.set_experiment(f"/Users/{DA.username}/model-serving-experiment")

        with mlflow.start_run(run_name="model-serving-run") as run:
            # Initialize the Random Forest classifier
            rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

            # Fit the model on the training data
            rf_classifier.fit(X_train, y_train)

            # Make predictions on the test data
            y_pred = rf_classifier.predict(X_test)

            # Enable automatic logging of input samples, metrics, parameters, and models
            mlflow.sklearn.autolog(log_input_examples=True, silent=True)
            # Calculate F1 score with 'macro' averaging for multiclass
            mlflow.log_metric("test_f1", f1_score(y_test, y_pred, average="macro"))
            # mlflow.log_metric("test_f1", f1_score(y_test, y_pred))

            mlflow.sklearn.log_model(
                rf_classifier,
                artifact_path="model-artifacts",
                input_example=X_train[:3],
                signature=infer_signature(X_train, y_train),
            )

            model_uri = f"runs:/{run.info.run_id}/model-artifacts"

        # Modify the registry uri to point to Unity Catalog
        mlflow.set_registry_uri("databricks-uc")

        # Define the model name
        model_name = (
            f"{DA.catalog_name}.{DA.schema_name}.my_model_{DA.unique_name('-')}"
        )

        # Register the model in the model registry
        registered_model = mlflow.register_model(model_uri=model_uri, name=model_name)

    # Initialize an MLflow Client
    mlflow_client = MlflowClient()

    # Solves the following edge case: A user deletes a model version and then tries to set an alias for that model version. The end result is to grab the latest model version starting at 1 and going to 100
    for i in range(1, 101):
        try:
            version_number = i  # Replace with your target version number

            # Set an alias for the specified model version
            alias_name = "Staging"
            mlflow_client.set_registered_model_alias(
                name=model_name, alias=alias_name, version=version_number
            )
            print(
                f"Found version {version_number} as the alias 'Staging'. Serving this version of the model."
            )
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Trying version {version_number + 1}...")

    model_serving_client = get_deploy_client("databricks")
    # endpoint_name = f"{DA.schema_name}-endpoint"  # DO NOT CHANGE
    endpoint_name = endpoint_name = re.sub(r'[^a-zA-Z0-9-_]', '-', f"{DA.username}-endpoint")[:63]  # Ensure endpoint name is within 63 characters

    try:
        # Attempt to get the endpoint
        existing_endpoint = model_serving_client.get_endpoint(endpoint_name)

        print(f"Endpoint '{endpoint_name}' already exists.")
        print(f"Using the existing endpoint with model version {version_number}")
    except Exception as e:
        # If not found, create the endpoint
        if "RESOURCE_DOES_NOT_EXIST" in str(e):
            print(f"Creating a new endpoint: {endpoint_name}")
            endpoint = model_serving_client.create_endpoint(
                name=endpoint_name,
                config={
                    "served_entities": [
                        {
                            "name": "my-model",
                            "entity_name": model_name,
                            "entity_version": version_number,  # The latest version number
                            "workload_size": "Small",
                            "scale_to_zero_enabled": True,
                        }
                    ],
                    "traffic_config": {
                        "routes": [
                            {"served_model_name": "my-model", "traffic_percentage": 100}
                        ]
                    },
                },
            )
        else:
            print(f"An error occurred: {e}")

        # The following code will restrict users from deleting the endpoint. Curriculum Development decided to limit the number of users per workspace instead.

        #   #update permissions so all users can query the endpoint
        endpoint_id = model_serving_client.get_endpoint(endpoint=endpoint_name).id
        DATABRICKS_INSTANCE = (
            dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()
        )
        TOKEN = (
            dbutils.notebook.entry_point.getDbutils()
            .notebook()
            .getContext()
            .apiToken()
            .get()
        )
        # API endpoint for retrieving permissions
        url = f"{DATABRICKS_INSTANCE}/api/2.0/permissions/serving-endpoints/{endpoint_id}"

        # Headers for the request
        headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

        # Restrict access to query-only
        payload = {
            "access_control_list": [
                {"group_name": "users", "permission_level": "CAN_QUERY"},
                {"user_name": DA.username, "permission_level": "CAN_QUERY"},
            ]
        }

        # Send the PATCH request to update permissions
        requests.patch(url, headers=headers, data=json.dumps(payload))

        print(
            f"Model serving endpoint is in state Creating. Please wait a few minutes for the endpoint to be ready."
        )

# COMMAND ----------

# Initialize DBAcademyHelper
DA = DBAcademyHelper() 
DA.init()
