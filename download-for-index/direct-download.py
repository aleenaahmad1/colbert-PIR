#Sends request and uses Wayback machine to directly download a given URL

import os
import pandas as pd
import requests
import time

# File paths
filename_csv = "failed_downloads_2.csv"  # Replace with actual filename
doc_csv = r"data\doc.csv"  # Replace with actual filename
output_directory = "profile-files"

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Load CSV files
filename_df = pd.read_csv(filename_csv)  # Contains 'Filename' column
doc_df = pd.read_csv(doc_csv, delimiter='\t')  # Contains 'Url' and 'DocIndex'

# Convert to dictionary for quick lookup
doc_map = dict(zip(doc_df['DocIndex'].astype(str), doc_df['Url']))

# Function to fetch content from a URL
def fetch_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    return None

# Function to attempt downloading from Wayback Machine
def fetch_from_wayback(original_url):
    wayback_url = f"https://web.archive.org/web/{original_url}"
    return fetch_content(wayback_url)

# Process each document ID
for index, row in filename_df.iterrows():
    doc_id = str(row['Filename'])  # Convert to string to match DocIndex format
    url = doc_map.get(doc_id)  # Get corresponding URL
    
    if not url:
        print(f"Skipping {doc_id}: URL not found.")
        continue

    content = fetch_content(url)

    # If original URL fails, try Wayback Machine
    if content is None:
        print(f"Original URL failed for {doc_id}, trying Wayback Machine...")
        content = fetch_from_wayback(url)

    if content:
        file_path = os.path.join(output_directory, f"{doc_id}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {file_path}")
    else:
        print(f"Failed to download: {doc_id}")

    time.sleep(1)  # Avoid overwhelming the server

print("Download process complete.")
