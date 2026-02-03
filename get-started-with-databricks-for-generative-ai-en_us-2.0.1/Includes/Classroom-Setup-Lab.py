# Databricks notebook source
# MAGIC %run ./Classroom-Setup-Common

# COMMAND ----------

DA = DBAcademyHelper()
DA.init()

# COMMAND ----------

DA.eval_set = pd.DataFrame([
    {
        "inputs": {
            "messages": [
                {
                    "role": "user",
                    "content": """
                        What is the syntax for using the next_day function in Databricks SQL and Databricks Runtime, and what arguments does it take?
                    """
                }
            ]
        },
        "expected": {
            "expected_response": """
                The syntax for using the `next_day` function in Databricks SQL and Databricks Runtime is as follows:

                `next_day(expr, dayOfWeek)`

                The `next_day` function takes two arguments:

                * `expr`: A DATE expression.
                * `dayOfWeek`: A STRING expression identifying a day of the week.

                The `dayOfWeek` argument must be one of the following (case insensitive): 'SU', 'SUN', 'SUNDAY', 'MO', 'MON', 'MONDAY', 'TU', 'TUE', 'TUESDAY', 'WE', 'WED', 'WEDNESDAY', 'TH', 'THU', 'THURSDAY', 'FR', 'FRI', 'FRIDAY', 'SA', 'SAT', 'SATURDAY'.

                The function returns the first date which is later than `expr` and named as in `dayOfWeek`. In Databricks Runtime, if `spark.sql.ansi.enabled` is false, the function returns NULL instead of an error for a malformed `dayOfWeek`.
            """
        }
    },
    {
        "inputs": {
            "messages": [
                {
                    "role": "user",
                    "content": """
                        Can I now use classic keyboard shortcuts in the new editor?
                    """
                }
            ]
        },
        "expected": {
            "expected_response": """
                Yes, as of July 2023, Databricks has introduced a new setting that allows you to use the classic keyboard shortcuts from the previous editor while still benefiting from the features of the new editor, such as autocomplete as you type, syntax highlighting, code formatting, and more. To access this setting, open the editor configuration and toggle Notebook editor shortcuts mode to Classic (Code Mirror).
            """
        }
    },
    {
        "inputs": {
            "messages": [
                {
                    "role": "user",
                    "content": """
                        How can I read data from a Parquet file using Databricks in a Python notebook?
                    """
                }
            ]
        },
        "expected": {
            "expected_response": """
                To read data from a Parquet file using Databricks in a Python notebook, you can use the `spark.read.parquet()` function. Here's a simple example:

                python
                # Import the SparkSession class
                from pyspark.sql import SparkSession

                # Create a SparkSession object
                spark = SparkSession.builder.appName('ParquetReader').getOrCreate()

                # Replace 'path_to_your_parquet_file' with the actual path to your Parquet file
                parquet_file_path = 'path_to_your_parquet_file'

                # Read the Parquet file
                df = spark.read.parquet(parquet_file_path)

                # Show the data
                df.show()
                

                In this example, replace `'path_to_your_parquet_file'` with the actual path to your Parquet file. This could be a local file path on your Databricks workspace, or a path to a file stored in a cloud storage service like AWS S3 or Azure Data Lake Storage.

                Remember to install the necessary libraries and set up your Databricks workspace before running this code. For more information on how to do this, refer to the Databricks documentation.
            """
        }
    },
    {
        "inputs": {
            "messages": [
                {
                    "role": "user",
                    "content": """
                        How can I create a workspace experiment using the Databricks UI and what are the steps to log runs to these experiments?
                    """
                }
            ]
        },
        "expected": {
            "expected_response": """
                To create a workspace experiment using the Databricks UI, follow these steps:
                1. Click Workspace in the sidebar.
                1. Navigate to the folder in which you want to create the experiment.
                1. Right-click on the folder and select Create > MLflow experiment.
                1. In the Create MLflow Experiment dialog, enter a name for the experiment and an optional artifact location.
                1. Click Create.

                To log runs to workspace experiments, you can use the MLflow API or the Databricks Terraform provider with databricks_mlflow_experiment. For instructions on logging runs to workspace experiments, see the Logging example notebook in the Databricks documentation.
            """
        }
    }
])
