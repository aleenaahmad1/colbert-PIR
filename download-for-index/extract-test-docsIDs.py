#from ALL the test files of each bucket, extracts the unique TEST docIDs and stores into a csv file: (all_unique_docIDs.csv)
#returns the number of unique docIDs (to determine if indexing should be split into parts or together)
import pandas as pd
import ast
import glob

# Get all test files
test_files = glob.glob("test_*.csv")

# Set to store all unique document IDs
all_unique_doc_ids = set()

def extract_doc_ids_from_candilist(candi_list):
    """
    Extract document IDs from a CandiList string formatted as a Python list
    """
    try:
        # Convert string representation of list to actual list
        doc_ids = ast.literal_eval(candi_list)
        return doc_ids
    except (ValueError, SyntaxError):
        # Return empty list if parsing fails
        return []

# Process each test file
for file in test_files:
    # Read CSV
    df = pd.read_csv(file)

    # Ensure CandiList column exists
    if "CandiList" not in df.columns:
        continue

    # Extract document IDs from CandiList column
    unique_doc_ids = set()
    
    for candi_list in df["CandiList"].dropna():
        doc_ids = extract_doc_ids_from_candilist(candi_list)
        unique_doc_ids.update(doc_ids)

    # Save unique doc IDs from this test file
    bucket_label = file.split("test_")[1].replace(".csv", "")
    output_file = f"unique_docs_{bucket_label}.csv"
    print(f"Number of unique test doc IDs for {file}:  {len(unique_doc_ids)}")
    pd.DataFrame(unique_doc_ids, columns=["DocID"]).to_csv(output_file, index=False)

    # Merge into the global unique doc ID set
    all_unique_doc_ids.update(unique_doc_ids)

# Save all unique doc IDs across all buckets
pd.DataFrame(all_unique_doc_ids, columns=["DocID"]).to_csv("all_unique_docIDs.csv", index=False)

# Print total count of unique document IDs
total_unique_docs = len(all_unique_doc_ids)
print(f"Total unique document IDs across all test files: {total_unique_docs}")
