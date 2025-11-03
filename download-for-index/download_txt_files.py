#Files downloaded and stored on Github Repo (downloaded from URLs in progress.json)
#This code downloads txt files from Github repo
#Input: CSV files of doc indexes to download, URL of txt files directory in repo, directory name to save files to, csv file name for failed_downloads

import csv
import os
import requests

# GitHub repo details (modify accordingly)
USERNAME = "aleenaahmad1"
REPO = "Test-Rafay"
BRANCH = "main"  # Change if needed
BASE_URL = f"https://raw.githubusercontent.com/shimroo/Test-Aleena/refs/heads/main/downloaded_txt/" #change Test-Aleena to Test-Rafay if needed

# Paths
CSV_FILE = "" #CSV file with list of doc indexes to be downloaded
SAVE_DIR = "profile-files"
FAILED_CSV = "failed_downloads_2.csv"

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Counters
total_files = 0
successful_downloads = 0
failed_downloads = 0
failed_files = []

# Read CSV file and process
with open(CSV_FILE, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        filename = row[0].strip()  # Get the filename
        file_url = BASE_URL + + filename + ".txt"
        # print(file_url)
        save_path = os.path.join(SAVE_DIR, filename)
        total_files += 1

        try:
            response = requests.get(file_url, stream=True)

            if response.status_code == 200:
                # Write the file content
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                successful_downloads += 1
                print(f"✅ Downloaded: {filename}")
            else:
                print(f"❌ File not found: {filename} (HTTP {response.status_code})")
                failed_files.append(filename)
                failed_downloads += 1

        except Exception as e:
            print(f"⚠️ Error downloading {filename}: {e}")
            failed_files.append(filename)
            failed_downloads += 1

# Save failed downloads to a CSV file
if failed_files:
    with open(FAILED_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Filename"])  # Header
        for failed_file in failed_files:
            writer.writerow([failed_file])

# Summary Report
print("\n📊 Download Summary:")
print(f"📁 Total files: {total_files}")
print(f"✅ Successfully downloaded: {successful_downloads}")
print(f"❌ Failed downloads: {failed_downloads}")

if failed_downloads > 0:
    print(f"⚠️ A list of missing files has been saved in '{FAILED_CSV}'.")

