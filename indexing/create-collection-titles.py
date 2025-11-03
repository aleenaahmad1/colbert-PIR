import os
import re
import pandas as pd

def preprocess_text(text):
    # Lowercase
    text = text.lower()

    # Remove boilerplate phrases (example)
    boilerplate_phrases = ["copyright", "all rights reserved", "terms of service"]
    for phrase in boilerplate_phrases:
        text = text.replace(phrase, "")

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text

def build_collection_with_titles():
    base_path = 'missed-txt-files'
    collection_file = 'missed_collection.tsv'
    
    # Read doc.csv to get titles
    try:
        doc_df = pd.read_csv(r'data\doc.csv', delimiter='\t')
        # Create a dictionary for quick title lookups
        title_dict = dict(zip(doc_df['DocIndex'].astype(str), doc_df['Title']))
    except Exception as e:
        print(f"Error reading doc.csv: {e}")
        return
    
    # Track statistics
    processed_count = 0
    missing_title_count = 0
    
    # Open the collection file for writing
    with open(collection_file, 'w', encoding='utf-8') as collection:
        # Write header
        collection.write("docID\ttitle\tcontent\n")
        
        # Process each file
        for filename in os.listdir(base_path):
            if filename.endswith('.txt'):
                docID = os.path.splitext(filename)[0]
                file_path = os.path.join(base_path, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        content = preprocess_text(content)
                        
                        # Get title from dictionary
                        title = title_dict.get(docID, "")
                        if not title:
                            missing_title_count += 1
                            print(f"Warning: No title found for docID: {docID}")
                            title = "NO_TITLE"  # Placeholder for missing titles
                        
                        # Preprocess title as well
                        title = preprocess_text(title)
                        
                        # Write to collection file in the format: docID\ttitle\tcontent
                        collection.write(f"{docID}\t{title}\t{content}\n")
                        
                        processed_count += 1
                        
                        # Print progress every 1000 documents
                        if processed_count % 1000 == 0:
                            print(f"Processed {processed_count} documents...")
                            
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
    
    # Print final statistics
    print("\nCollection Building Statistics:")
    print(f"Total documents processed: {processed_count}")
    print(f"Documents missing titles: {missing_title_count}")
    print(f"Collection saved to '{collection_file}'")

if __name__ == "__main__":
    build_collection_with_titles()