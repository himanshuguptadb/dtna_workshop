## Challenge Questions:

1. How would you update **Lab 01b - Flattening Parsed PDFs** to avoid rewriting the table each time? This will move your POC from a complete overwrite to updating only when new PDFs land in your volume.

_Answer: You can replace `CREATE OR REPLACE TABLE AS` with logic that uses `MERGE INTO` so that only new rows are appended. You can read more [here](https://docs.databricks.com/aws/en/delta/merge)._

2. How would you update your Job so you only process files when they land in the volume? This would allow for automatic pipeline runs to process your PDFs.

_Answer: You can add a triggering event for the Lakeflow Job under the  **Schedule and Triggers** option on the right._

3. Architect a workflow to include the Lakeflow Declarative Pipeline option. What are the limitations?

_Answer: Notice our workflow is completely separate from the Lakeflow Declarative Pipeline. However, we could add this pipeline as a dependency onto our second task that flattens the tables._