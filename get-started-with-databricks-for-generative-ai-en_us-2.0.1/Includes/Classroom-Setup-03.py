# Databricks notebook source
# MAGIC %pip install -qqq -U databricks-sdk databricks-langchain databricks-vectorsearch langsmith>=0.1.125 langchain==0.3.27 mlflow-skinny[databricks]>=3.4.0 
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ./Classroom-Setup-Common

# COMMAND ----------

DA = DBAcademyHelper()
DA.init()

# COMMAND ----------

import pandas as pd

DA.eval_set = pd.DataFrame([
    {
        "inputs": {"messages": [{"role": "user", "content": "personalized wooden name sign with app control"}]},
        "expectations": {"creative_enough": True},
    },
    {
        "inputs": {"messages": [{"role": "user", "content": "handmade lamp with remote dimming"}]},
        "expectations": {"creative_enough": True},
    },
    {
        "inputs": {"messages": [{"role": "user", "content": "ceramic planter with self-watering insert and moisture indicator"}]},
        "expectations": {"creative_enough": False},
    },
])
