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
# MAGIC # DEMO - Evaluation with MLflow
# MAGIC
# MAGIC After building the model, it is essential to evaluate its performance. In this demo, we will demonstrate how to use the **Agent Framework** to assess the model's performance. The example will show how to calculate built-in evaluation metrics and define custom metrics.
# MAGIC
# MAGIC **Learning Objectives:**
# MAGIC
# MAGIC *By the end of this demo, you will be able to:*
# MAGIC
# MAGIC * Load a model from the model registry for evaluation.
# MAGIC
# MAGIC * Identify common built-in evaluation metrics.
# MAGIC
# MAGIC * Define custom evaluation metrics.
# MAGIC
# MAGIC * Run an evaluation test and view the results using the UI or code.

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
# MAGIC ## Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC * To run this notebook, you need to use one of the following Databricks runtime(s): **17.3.x-cpu-ml-scala2.13**
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC Set up the classroom environment by installing the required libraries and datasets.

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-03

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prepare for Evaluation
# MAGIC
# MAGIC The first step is to load the model that will be used for evaluation. The RAG model we built in the previous demo was **registered in the UC model registry**.
# MAGIC
# MAGIC After loading the model, we will **define the evaluation dataset**. This dataset must include a **"request"** field to be used as the input query for the model. It typically also includes **"ground-truth" fields for response or context**. In this demo, to keep it simple, we will use only one request-response pair.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Load the Model
# MAGIC
# MAGIC Let's start by loading the model so that we can use it to generate responses and evaluate those responses later. Note that we will load a specific version of the model.

# COMMAND ----------

import mlflow
mlflow.set_registry_uri("databricks-uc")

model_uri = f"models:/{DA.catalog_name}.{DA.schema_name}.getstarted_genai_retrevial_demo/1"
print(model_uri)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Load Evaluation Dataset
# MAGIC
# MAGIC In this demo we will only use **"request" and "expected_response"**. For examples of using other fields, you can check [sample evaluation sets](https://docs.databricks.com/en/generative-ai/agent-evaluation/evaluation-set.html#sample-evaluations-sets). 
# MAGIC
# MAGIC Evaluation dataset is crucial for the accuracy of the evaluation. Some of the best practices are; 
# MAGIC * When developing an evaluation set, treat each sample as a unit test with a specific scenario and expected outcome, **including challenging examples and adversarial scenarios**. 
# MAGIC
# MAGIC * Ensure the evaluation set **reflects a variety of questions**, even beyond the application's primary domain, to prevent hallucinations or harmful responses. 
# MAGIC
# MAGIC * **High-quality, consistent human-generated labels are crucial**; achieve this by aggregating responses from multiple labelers and providing clear instructions to ensure consistency.

# COMMAND ----------

display(DA.eval_set)

# COMMAND ----------

import os
import mlflow
from mlflow.genai import evaluate
from mlflow.genai.scorers import Guidelines, RelevanceToQuery, Safety
import mlflow.pyfunc

os.environ["VS_INDEX_NAME"] = f"{DA.catalog_name}.{DA.schema_name}.product_embeddings"

# (1) Predict fn that calls your registered model

model = mlflow.pyfunc.load_model(model_uri)

# Predict function expected by mlflow.genai.evaluate()
@mlflow.trace
def predict_fn(messages):
    """
    messages: list of {role, content}
    Returns: assistant text (str) for scorers.
    """
    out = model.predict({"input": messages})

    # Databricks Responses shape: {"object":"response","output":[{message...}]}
    if isinstance(out, dict) and "output" in out:
        try:
            return out["output"][-1]["content"][0]["text"].strip()
        except Exception:
            pass  # fall through

    # Older shape: list of message dicts
    if isinstance(out, list):
        try:
            return out[-1]["content"][0]["text"].strip()
        except Exception:
            pass

    # Fallbacks
    if isinstance(out, str):
        return out.strip()
    if isinstance(out, dict):
        for k in ("answer", "response", "text", "output"):
            v = out.get(k)
            if isinstance(v, str):
                return v.strip()

    return str(out).strip()

# Guidelines scorer for creative_enough (boolean pass/fail)
creative_guidelines = Guidelines(
    name="creative_enough",
    guidelines="""The response must feel original and imaginative, not a paraphrase of the prompt.
It should introduce a concept or angle (e.g., theme, use-case, material pairing) beyond listing features.
Keep within ~250 words and avoid tool/planning narration."""
)

# (3) Run evaluation (eval_set has "inputs" and optional "expectations")
mlflow.set_experiment(f"/Users/{DA.username}/Retreival_Eval")
with mlflow.start_run(run_name="eval_guidelines") as eval_run:
    eval_results = evaluate(
        data=DA.eval_set, 
        predict_fn=predict_fn, 
        scorers=[
            creative_guidelines,     # pass/fail vs. our creative_enough label
            RelevanceToQuery(),      # built-in; no ground truth required
            Safety(),                # built-in; no ground truth required
        ]
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Model Evaluation

# COMMAND ----------

# MAGIC %md
# MAGIC ### Build-in Metrics
# MAGIC
# MAGIC Mosaic AI Agent Framework uses LLM-judges to evaluate the model using common evaluation metrics such as safety and relevance. Also, it calculates system metrics such as token count and latency.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Custom Metric
# MAGIC
# MAGIC Although the Agents Evaluation framework automatically calculates common evaluation metrics, there are instances where we may need to assess the model using custom metrics. In this section, we will define a custom metric to evaluate whether the **response** generated is creative or not.

# COMMAND ----------

from mlflow.genai.scorers import Guidelines

creativity_level = Guidelines(
    name="creativity_level",
    guidelines="""Your task is to determine whether the generated product idea is creative or not.
Grade the idea from 1 to 5, where 5 is very creative and 1 is very boring.
This is the output: {response}."""
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run Evaluation Test
# MAGIC
# MAGIC Please note that in the code below, we are logging the evaluation process using MLflow to enable viewing the results through the MLflow UI.

# COMMAND ----------

print(model_uri)
with mlflow.start_run(run_name="rag_eval_demo_04_01"):
    eval_results = mlflow.evaluate(
        data=DA.eval_set,
        model = model_uri,
        model_type = "databricks-agent",
        extra_metrics=[creativity_level]
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Review Evaluation Results
# MAGIC
# MAGIC We have two options for reviewing the evaluation results. The first option is to examine the metrics and tables directly using the results object. The second option is to review the results through the user interface (UI).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Review Results via the UI
# MAGIC
# MAGIC To view the results in the UI, follow these steps:
# MAGIC
# MAGIC - Click on the **"Experiment"** link displayed at the top of the previous code block's output for a simpler method.
# MAGIC
# MAGIC - Alternatively, you can navigate to "Experiments" in the left panel and locate the experiment registered with the title of this notebook.
# MAGIC
# MAGIC - View the overall metrics in the **Model Metrics** tab.
# MAGIC
# MAGIC - Examine detailed results for each assessment in the **Evaluation Results** tab.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Review Results Table

# COMMAND ----------

display(eval_results.metrics)

# COMMAND ----------

display(eval_results.tables['eval_results'])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Clean up Classroom
# MAGIC
# MAGIC **🚨 Warning:** Please refrain from deleting resources created in this demo, as they are required for upcoming demonstrations. To clean up the classroom assets, execute the classroom clean-up script provided in the final demo.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Summary
# MAGIC
# MAGIC In this demo, we demonstrated how to load a model from the model registry and evaluate its performance using both built-in metrics and custom metrics. As an example of a custom metric, we defined one that assesses the creativity of the generated response. After running the evaluation, we showed how to view the results using the MLflow UI and the result object table.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
