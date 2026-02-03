# Databricks notebook source
# MAGIC %run ./_common

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
import pyspark.pandas as ps

import re

from databricks.feature_engineering import FeatureEngineeringClient
from databricks.sdk import WorkspaceClient

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

import mlflow 
from mlflow.models.signature import infer_signature
from mlflow.deployments import get_deploy_client



import requests
import json

# COMMAND ----------

@DBAcademyHelper.add_method
def create_model_serving_endpoint(self, model_version):
    model_name = f"{my_catalog}.{my_schema}.gs_db_ml_LAB_{DA.unique_name('-')}"
    model_serving_client = get_deploy_client("databricks")
    endpoint_name = f"{DA.schema_name}-endpoint"  # DO NOT CHANGE

    try:
        # Attempt to get the endpoint
        existing_endpoint = model_serving_client.get_endpoint(endpoint_name)
        print(
            f"Endpoint '{endpoint_name}' already exists. Please use the UI to navigate to Serving in the left sidebar and query your endpoint."
        )






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
                            "entity_version": model_version,  # The latest version number
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
            dbutils.notebook.entry_point.getDbutils()
            .notebook()
            .getContext()
            .apiUrl()
            .get()
        )
        TOKEN = (
            dbutils.notebook.entry_point.getDbutils()
            .notebook()
            .getContext()
            .apiToken()
            .get()
        )
        # API endpoint for retrieving permissions
        url = (
            f"{DATABRICKS_INSTANCE}/api/2.0/permissions/serving-endpoints/{endpoint_id}"
        )

        # Headers for the request
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        }

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
