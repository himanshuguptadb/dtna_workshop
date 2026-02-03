# Databricks notebook source
# MAGIC %run ./_common

# COMMAND ----------

@DBAcademyHelper.add_method
def validate_table(self, name):
    if spark.catalog.tableExists(name):
        print(f'Validation of table {name} complete. No errors found.')
        return True
    else:
        raise AssertionError(f"The table {name} does not exist")

# COMMAND ----------

DA = DBAcademyHelper()
DA.init()
