#from the unique extracted docIDs -> filter the ones that are valid according to progress.json BEFORE downloading
import json
import pandas as pd

# Define file paths
unique_doc_ids_file = r"updated_buckets\all_unique_docIDs.csv"  # CSV file with unique docIDs
doc_csv_file = r"data\doc.csv"  # CSV mapping docIDs to URLs
progress_json_file = r"updated_buckets\progress.json"  # JSON file mapping URLs to True/False

# Load data
unique_docids_df = pd.read_csv(unique_doc_ids_file)
doc_df = pd.read_csv(doc_csv_file, delimiter='\t')

# Load JSON progress file
with open(progress_json_file, "r", encoding="utf-8") as f:
    progress_data = json.load(f)

# Merge unique_docIDs with doc.csv to get corresponding URLs
merged_df = unique_docids_df.merge(doc_df[['Url', 'DocIndex']], left_on='DocID', right_on='DocIndex', how='left')

# Filter out rows where the URL has a True value in progress.json
filtered_df = merged_df[merged_df['Url'].isin([url for url, status in progress_data.items() if status])]

# Keep only relevant columns
filtered_df = filtered_df[['DocID']]

# Save the filtered list to a new CSV file
filtered_csv_file = "filtered_unique_docIDs.csv"
filtered_df.to_csv(filtered_csv_file, index=False)

print(f"Filtered CSV saved as {filtered_csv_file}. Kept {len(filtered_df)} rows.")

