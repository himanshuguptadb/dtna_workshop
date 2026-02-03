# Databricks notebook source
# MAGIC %run ./_common

# COMMAND ----------

DA = DBAcademyHelper()
DA.init()

# COMMAND ----------

vol_name = 'build_agents_vol'

# COMMAND ----------

spark.sql(f'USE CATALOG {DA.catalog_name}')
spark.sql(f'USE SCHEMA {DA.schema_name}')
spark.sql(f'CREATE VOLUME IF NOT EXISTS {vol_name}')

# COMMAND ----------

try: 
    volume_path = f"/Volumes/{DA.catalog_name}/{DA.schema_name}/{vol_name}"
    dst_uri_1 = f"dbfs:{volume_path}/_single_pdf"
    dst_uri_2 = f"dbfs:{volume_path}/_multiple_pdfs"
    dbutils.fs.mkdirs(dst_uri_1)
    dbutils.fs.mkdirs(dst_uri_2)
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
        single_vol_path = f"{volume_path}/_single_pdf"
        muli_vol_path = f"{volume_path}/_multiple_pdfs" 
        vol_path_list = [single_vol_path, muli_vol_path]

        file_map = {
            single_vol_path: [available_files[0]],
            muli_vol_path: [available_files[0], available_files[1]]
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

marketplace_source_folder_1 = "/Volumes/databricks_arxiv_sample_articles/v01/arxiv-articles/"
marketplace_source_folder_2 = "/Volumes/dbacademy_arxiv_sample_articles/v01/arxiv-articles"
marketplace_source_folder_3 = "/Volumes/dbacademy_arxiv/v01/arxiv-articles"

src_folders = [marketplace_source_folder_2, marketplace_source_folder_3, marketplace_source_folder_1]

for marketplace_source_folder in src_folders:
    try: 
        pipeline = CopyPipeline(
            folder_name=marketplace_source_folder,
            volume_path=f"{volume_path}" 
        )
        pipeline.run()
        print(f"✅ Successfully copied files to {marketplace_source_folder}!")
        break 
    except Exception as e: 
        print(f"Error: {e}")
        if marketplace_source_folder == marketplace_source_folder_1:
            print(f"Tried {marketplace_source_folder_1}, but couldn't find files.")
            print(f"Now trying {marketplace_source_folder_2}")
        else: 
            print(f"❌ Tried seraching in {marketplace_source_folder_1} and {marketplace_source_folder_2} and failed to run pipeline. Try checking the naming and source file in the Includes folder.")

# COMMAND ----------

import requests

class TileManager:
    def __init__(self, host: str, headers: dict):
        self.host = host.rstrip('/')
        self.headers = headers

    def get_tile(self, tile_id: str):
        url = f"{self.host}/api/2.0/tiles/{tile_id}"
        payload = {"tile_id": tile_id}
        resp = requests.get(url, headers=self.headers, json=payload)
        resp.raise_for_status()
        return resp.json()

    def get_endpoint_name(self, tile_id: str):
        tile = self.get_tile(tile_id)
        return tile.get('serving_endpoint_name')

    def list_endpoints(self):
        url = f"{self.host}/api/2.0/serving-endpoints"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def list_tiles(self, next_page_token=None):
        url = f"{self.host}/api/2.0/tiles"
        params = {"page_token": next_page_token} if next_page_token else {}
        resp = requests.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def list_all_tiles(self):
        res = []
        next_page_token = None
        while True:
            tiles = self.list_tiles(next_page_token)
            res.extend(tiles.get("tiles", []))
            next_page_token = tiles.get("next_page_token")
            if not next_page_token:
                break
        return res

    def delete_tile_endpoint(self, endpoint_name: str):
        try:
            url = f"http://127.0.0.1:7073/api/2.0/tile-endpoints/{endpoint_name}"
            resp = requests.delete(url, headers=self.headers)
            resp.raise_for_status()
            print(f"Deleted: {endpoint_name}")
        except Exception as e:
            print(f"Error deleting tile endpoint '{endpoint_name}': {e}")

    def delete_tile_endpoint_from_tile_id(self, tile_id: str):
        try:
            endpoint_name = self.get_endpoint_name(tile_id)
            self.delete_tile_endpoint(endpoint_name)
        except Exception as e:
            print(f"Error deleting tile endpoint from tile ID '{tile_id}': {e}")

    def delete_tile(self, tile_id: str):
        try:
            url = f"{self.host}/api/2.0/tiles/{tile_id}"
            payload = {"tile_id": tile_id}
            resp = requests.delete(url, headers=self.headers, json=payload)
            resp.raise_for_status()
            if resp.json() == {}:
                print("Successfully deleted tile")
        except Exception as e:
            print(f"Error deleting tile '{tile_id}': {e}")

    def get_tile_id_by_name(self, endpoint_name: str):
        """Return the tile_id for a given tile name (serving endpoint name)."""
        try:
            tiles = self.list_all_tiles()
            tile_id = next((tile['tile_id'] for tile in tiles if tile.get('name') == endpoint_name), None)

            if tile_id:
                return tile_id
            else:
                print(f"Tile with name '{endpoint_name}' not found.")
                return None
        except Exception as e:
            print(f"Error getting tile ID for endpoint '{endpoint_name}': {e}")
            return None
    def full_delete_with_tile_id(self, tile_id: str):
        try:
            self.delete_tile_endpoint_from_tile_id(tile_id)
            self.delete_tile(tile_id)
        except Exception as e:
            print(f"Error deleting tile '{tile_id}': {e}")
    
    def full_delete_with_endpoint_name(self, endpoint_name: str):
        try:
            tile_id = self.get_tile_id_by_name(endpoint_name)
            self.delete_tile(tile_id)
        except Exception as e:
            print(f"Error deleting tile endpoint '{endpoint_name}': {e}")

# COMMAND ----------

def delete_agent_resources():
    token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
    host = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()

    headers = {
    "Authorization": f"Bearer {token}"
    }

    tm = TileManager(host, headers)

    tiles = tm.list_all_tiles()
    number_of_tiles = len(tiles)
    if not tiles:
        print("No tiles found. Nothing to delete.")
        return None
    else:
        for agent_id in range (number_of_tiles):
            tile_id = tiles[agent_id]['tile_id']
            # print(f"you are about to delete agent with ID: {tile_id}")
            tm.full_delete_with_tile_id(tile_id)
