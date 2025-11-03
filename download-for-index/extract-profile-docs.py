#from train records, extract clicked doc IDs
import os
import shutil
import pandas as pd

# Define the folder where CSV files are stored
folder_path = "updated_buckets"  # Change this to the actual path
output_file = "unique_clicked_docIDs.csv"

# Set to store unique docIDs
unique_doc_ids = set()

# Loop through all train CSV files
for file in os.listdir(folder_path):
    if file.startswith("train_") and file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        
        # Extract clicked document IDs (DocIndex column)
        clicked_doc_ids = df["DocIndex"].dropna().astype(str).unique()
        unique_doc_ids.update(clicked_doc_ids)


txt_dirs = ["txt-files", "new-txt-files"]  # Directories to check for downloaded files
output_dir = "profile-files"  # Directory to copy existing files
missing_docs_file = "missing_docIDs.csv"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Track found and missing doc IDs
found_doc_ids = set()
missing_doc_ids = set(unique_doc_ids)

# Check for each doc ID in the specified directories
for doc_id in unique_doc_ids:
    file_name = f"{doc_id}.txt"
    for txt_dir in txt_dirs:
        file_path = os.path.join(txt_dir, file_name)
        if os.path.exists(file_path):
            shutil.copy(file_path, output_dir)
            found_doc_ids.add(doc_id)
            missing_doc_ids.discard(doc_id)
            break  # Stop checking once found

# Save missing doc IDs to CSV
missing_doc_ids_df = pd.DataFrame(sorted(missing_doc_ids), columns=["MissingDocID"])
missing_doc_ids_df.to_csv(missing_docs_file, index=False)

print(f"Copied {len(found_doc_ids)} files to '{output_dir}'.")
print(f"{len(missing_doc_ids)} doc IDs were not found and written to '{missing_docs_file}'.")
