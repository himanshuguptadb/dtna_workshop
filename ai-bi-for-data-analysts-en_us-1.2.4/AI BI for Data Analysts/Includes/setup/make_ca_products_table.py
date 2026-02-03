# Databricks notebook source
# MAGIC %sql
# MAGIC USE CATALOG dbacademy;  -- Modify to use DBACADEMY in Vocareum
# MAGIC USE SCHEMA ops;
# MAGIC
# MAGIC -- Creates View of keys + values
# MAGIC CREATE OR REPLACE TEMP VIEW user_info AS
# MAGIC SELECT map_from_arrays(collect_list(key), collect_list(value))
# MAGIC FROM meta;
# MAGIC
# MAGIC -- Creates MAP object of ops table key + values using the view
# MAGIC DECLARE OR REPLACE DA MAP<STRING,STRING>;
# MAGIC SET VAR DA = (SELECT * FROM user_info);
# MAGIC
# MAGIC -- Set default schema for the user  
# MAGIC USE SCHEMA IDENTIFIER(DA.schema_name);
# MAGIC
# MAGIC -- Create the ca_products table
# MAGIC
# MAGIC DROP TABLE IF EXISTS ca_products;
# MAGIC
# MAGIC CREATE TABLE ca_products (productid string, productname string, listprice float);
# MAGIC
# MAGIC INSERT INTO
# MAGIC   ca_products (productid, productname, listprice)
# MAGIC VALUES
# MAGIC   ('JQ9322', 'TableSaw', 24.99),
# MAGIC   ('A802a', 'Mill', 10.17),
# MAGIC   ('EE05x', 'Press', 363.02),
# MAGIC   ('R9S10', 'Lathe', 43.83),
# MAGIC   ('BC111d', 'Drill', 63.28),
# MAGIC   ('W8931', 'Planer', 45.22),
# MAGIC   ('Q28R3', 'Grinder', 176.33),
# MAGIC   ('MDb304', 'CAD System', 502.80),
# MAGIC   ('OR307p', 'Kazoo', 0.99); 
# MAGIC
