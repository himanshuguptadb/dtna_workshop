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
# MAGIC ## Get Started with Databricks for Machine Learning
# MAGIC
# MAGIC In this course, you will learn basic skills that will allow you to use the Databricks Data Intelligence Platform to perform a simple data science and machine learning workflow. You will be given a tour of the workspace, and you will be shown how to work with notebooks. You will train a baseline model with AutoML and transition the best model to production. Finally, the course will also introduce you to MLflow, feature store, and workflows, and demonstrate how to train and manage an end-to-end machine learning lifecycle.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Prerequisites
# MAGIC The content was developed for participants with these skills/knowledge/abilities:  
# MAGIC - A beginner-level understanding of Python.
# MAGIC - Basic understanding of DS/ML concepts (e.g. classification and regression models), common model metrics (e.g. F1-score), and Python libraries (e.g. scikit-learn and XGBoost). 
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Course Agenda  
# MAGIC The following modules are part of the **Get Started with Databricks for Machine Learning** course by **Databricks Academy**.
# MAGIC
# MAGIC | # | Module Name | Lesson Name |
# MAGIC |---|-------------|-------------|
# MAGIC | 1 | **[Databricks Overview]($./M01 - Databricks Overview)** | • *Lecture:* Databricks Data Intelligence Platform <br> • [Demo: 01 - Databricks Workspace Walkthrough]($./M01 - Databricks Overview/01 - Databricks Workspace Walkthrough) |
# MAGIC | 2 | **[Databricks for Machine Learning]($./M02 - Databricks for Machine Learning)** | • *Lecture:* Introduction to Machine Learning on Databricks <br>•  *Lecture:* EDA and Feature Engineering on Databricks <br> • [Demo: 01 - EDA and Feature Engineering]($./M02 - Databricks for Machine Learning/01 - EDA and Feature Engineering) <br> • *Lecture:* Introduction to MLflow on Databricks <br> • [Demo: 02 - Tracking and Managing Models with MLflowL]($./M02 - Databricks for Machine Learning/02 - Tracking and Managing Models with MLflow) <br> • *Lecture:* Introduction to Mosaic AI AutoML <br> • [Demo: 03 - Experimentation with Mosaic AI AutoML]($./M02 - Databricks for Machine Learning/03 - Experimentation with Mosaic AI AutoML) <br> • *Lecture:* Introduction to Mosaic AI Model Serving <br> • [Demo: 04 - Getting Started with Mosaic AI Model Serving]($./M02 - Databricks for Machine Learning/04 - Getting Started with Mosaic AI Model Serving) |
# MAGIC | 3 | **[Comprehensive Lab]($./M03 - Comprehensive Lab)** | • *Lecture:* Getting Started with Databricks for Machine Learning <br> • [Lab: Getting Started with Databricks for Machine Learning]($./M03 - Comprehensive Lab/3.Lab - Getting Started with Databricks for Machine Learning)
# MAGIC
# MAGIC ## Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC * Use Databricks Runtime version: **`16.4.x-cpu-ml-scala2.12`** for running all demo and lab notebooks.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
