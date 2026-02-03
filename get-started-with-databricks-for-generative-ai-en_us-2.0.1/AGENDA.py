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
# MAGIC ## Get Started with Databricks for Generative AI
# MAGIC
# MAGIC This course offers a practical introduction to the Mosaic AI platform, focusing on its key components and features for building and deploying generative AI systems. Participants will learn how Databricks facilitates the development of scalable generative AI solutions and explore Mosaic AI tools such as Vector Search, the Agent Framework, and MLflow’s generative AI capabilities for model tracking and logging. This course includes hands-on experience in constructing and evaluating Retrieval-Augmented Generation (RAG) pipelines, deploying generative AI agents, and leveraging evaluation frameworks to optimize performance. By the end of the course, learners will be equipped with the skills to design, deploy, and monitor common generative AI applications using Mosaic AI.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Prerequisites
# MAGIC The content was developed for participants with these skills/knowledge/abilities:  
# MAGIC - Basic knowledge of generative AI engineering topics is recommended.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Course Agenda  
# MAGIC The following modules are part of the **Get Started with Databricks for Generative AI** course by **Databricks Academy**.
# MAGIC
# MAGIC | # | Module Name | Lesson Name |
# MAGIC |---|-------------|-------------|
# MAGIC | 1 | **Module 1: Databricks Mosaic AI Overview** | • *Lecture:* The Generative AI Opportunity <br> • *Lecture:* Databricks Mosaic AI Platform |
# MAGIC | 2 | **[Module 2: Prompt Engineering in AI Playground]($./2 - Prompt Engineering in AI Playground)** | • *Lecture:* Prompt Engineering Basics <br> • [Demo: Prompt Engineering in AI Playground]($./2 - Prompt Engineering in AI Playground/2.1 - Prompt Engineering in AI Playground) |
# MAGIC | 3 | **[Module 3: Build and Register a Retrieval Pipeline]($./3 - Build and Register a Retrieval Pipeline)** | • *Lecture:* Retrieval Augmented Generation (RAG) Fundamentals <br> • *Lecture:* Mosaic AI Vector Search <br> • *Lecture:* MLFlow for GenAI <br> • [Demo: Build and Register a RAG Model]($./3 - Build and Register a Retrieval Pipeline/3.1 - Build and Register a RAG Model) |
# MAGIC | 4 | **[Module 4: Evaluating and Deploying AI Systems]($./4 - Evaluating and Deploying AI Systems)** | • *Lecture:* End-to-end Evaluation <br> • [Demo: Evaluation with MLflow]($./4 - Evaluating and Deploying AI Systems/4.1 - Evaluation with MLflow) <br> • *Lecture:* Real-time Deployment with Model Serving <br> • [Demo: Real-time Deployment with Model Serving]($./4 - Evaluating and Deploying AI Systems/4.2 - Real-time Deployment with Model Serving) |
# MAGIC | 5 | **[Module 5: End-to-end RAG Pipeline on Databricks]($./5 - End-to-end RAG Pipeline on Databricks)** | • [Lab: End-to-end RAG Pipeline]($./5 - End-to-end RAG Pipeline on Databricks/LAB - End-to-end RAG Pipeline) | 
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC * Use Databricks Runtime version: **`17.3.x-cpu-ml-scala2.13`** for running all demo and lab notebooks.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
