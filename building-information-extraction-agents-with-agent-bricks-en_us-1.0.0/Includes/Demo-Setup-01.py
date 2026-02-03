# Databricks notebook source
!pip install databricks-sdk
dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ./_common

# COMMAND ----------

DA = DBAcademyHelper()
DA.init()

# COMMAND ----------

vol_name = 'demo_build_agents_vol'

# COMMAND ----------

spark.sql(f'USE CATALOG {DA.catalog_name}')
spark.sql(f'USE SCHEMA {DA.schema_name}')
spark.sql(f'CREATE VOLUME IF NOT EXISTS {vol_name}')

# COMMAND ----------

try: 
    volume_path = f"/Volumes/{DA.catalog_name}/{DA.schema_name}/{vol_name}"
    dst_uri_1 = f"dbfs:{volume_path}/_single_pdf"
    dbutils.fs.mkdirs(dst_uri_1)
except: 
    raise Exception("Either could not find volume or make directories. Please check the source folder.")

# COMMAND ----------

import os
from pathlib import Path
from pyspark.dbutils import DBUtils

class CopyPipeline:
    def __init__(
        self,
        folder_name="",
        volume_path=""
    ):
        self.folder_name = folder_name
        self.volume_path = volume_path.rstrip("/")

    def run(self):
        """
        1) Wipe out whatever’s currently in the target volume directory
        2) Re-create it
        3) Copy in all local notebooks
        """
        spark.sql(f'USE CATALOG {DA.catalog_name}')
        spark.sql(f'USE SCHEMA {DA.schema_name}')
        self._clean_volume_dir()
        print("copying files...")
        self._copy_files()
        print("copied files!")

    def get_available_files(self):
        """Recursively list all files under `self.folder_name` on the driver
        that start with 'Demo' or 'Lab'."""
        files_list = []
        for root, _, files in os.walk(self.folder_name):
            print(f"Grabbing files from {root}")
            for fname in files:
                files_list.append(os.path.join(root, fname))
        return files_list

    def _clean_volume_dir(self):
        """Delete the entire target directory in DBFS (if it exists), then recreate it."""
        dst_uri = f"dbfs:{self.volume_path}"
        # Remove any existing directory
        print("Cleaning directory...")
        try:
            dbutils.fs.rm(dst_uri, recurse=True)
            # print(f"Deleted existing volume directory: {dst_uri}")
        except Exception:
            # ignore if it didn’t exist
            pass
        # Re-make the directory
        dbutils.fs.mkdirs(dst_uri)
        # print(f"Recreated volume directory:   {dst_uri}")
        print("Cleaned directory!")

    def _copy_files(self):
        """
        Copy each local file up into the UC volume.
        Any prior copies of the same name will already have been wiped by _clean_volume_dir().
        """
        available_files = self.get_available_files()

        # For this lab, we will create 2 directories. 
        single_vol_path = f"{volume_path}/demo_single_pdf"
        vol_path_list = [single_vol_path]

        file_map = {
            single_vol_path: [available_files[0]]
        }

        # Loop over each folder → its assigned files
        for vol_path, src_paths in file_map.items():
            for src in src_paths:
                stem = Path(src).stem
                ext  = Path(src).suffix or ""

                # Build destination under that specific volume path
                dst_path = f"{vol_path}/{stem}{ext}"

                src_uri = os.path.abspath(src)
                dst_uri = f"dbfs:{dst_path}"

                print(f"Copying {src_uri} ➔ {dst_uri}")
                dbutils.fs.cp(src_uri, dst_uri)
                print(f"Copied ➔ {src_uri}  →  {dst_uri}")

# COMMAND ----------

def check_if_labuser_is_here():
    username = DA.schema_name
    if username[-1].isdigit():
        return True 
    else:
        return False

# COMMAND ----------

# This logic is to account for different import naming of the ArXiv documents
user_check = check_if_labuser_is_here()
if user_check == True:
    marketplace_source_folder_1 = "/Volumes/databricks_arxiv_sample_articles/v01/arxiv-articles"
    marketplace_source_folder_2 = "/Volumes/databricks_arxiv_sample_articles/v01/arxiv-articles"
    src_folders = [
        marketplace_source_folder_1, 
        marketplace_source_folder_2
        ]
else:
    marketplace_source_folder_1 = "/Volumes/databricks_arxiv_sample_articles/v01/arxiv-articles"
    src_folders = [
        marketplace_source_folder_1
        ]

# COMMAND ----------

# Run the pipeline to copy files over to the user's volume 
for marketplace_source_folder in src_folders:
    try: 
        pipeline = CopyPipeline(
            folder_name=marketplace_source_folder,
            volume_path=f"{volume_path}" 
        )
        pipeline.run()
        print(f"✅ Successfully copied files from {marketplace_source_folder}!")
        break 
    except Exception as e: 
        print(f"Error: {e}")
        print(f"❌ Tried seraching in {marketplace_source_folder} and failed to run pipeline. Try checking the naming and source file in the Includes folder.")
