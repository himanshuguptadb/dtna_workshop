# Databricks notebook source
# This notebook performs feature engineering on tables created in Classroom-Setup-1.

# COMMAND ----------

# MAGIC %run ./_common

# COMMAND ----------

# %run ./Classroom-Setup-1

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

# COMMAND ----------

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

# COMMAND ----------

# Initialize DBAcademyHelper
DA = DBAcademyHelper() 
DA.init()
