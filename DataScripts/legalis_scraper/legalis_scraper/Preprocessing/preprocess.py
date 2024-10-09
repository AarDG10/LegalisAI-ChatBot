import json
import pandas as pd
import re

# Function to clean text by removing extra spaces, newlines, and special characters
def clean_text(text):
    # Remove newlines, tabs, and extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

# Load the JSON file into a DataFrame
with open('../spiders/data1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Display the initial data structure (optional)
print("Initial Data Sample:")
print(df.head())

# Drop rows with missing 'title' or 'summary'
df.dropna(subset=['title', 'summary'], inplace=True)

# Clean the 'title' and 'summary' columns (which are lists) by joining into strings and cleaning text
df['title'] = df['title'].apply(lambda x: clean_text(' '.join(x)))
df['summary'] = df['summary'].apply(lambda x: clean_text(' '.join(x)))

# Clean the 'source' column: If the value is not a string or is missing, fill with 'Unknown'
df['source'] = df['source'].apply(lambda x: x if isinstance(x, str) else 'Unknown')

# Clean the 'citation_links' column: Ensure all links are valid or fill with empty lists
df['citation_links'] = df['citation_links'].apply(lambda x: x if isinstance(x, list) else [])

# Annotate a 'case_type' column based on keywords in the title
def classify_case_type(title):
    if 'estate' in title.lower():
        return 'Real Estate'
    else:
        return 'Unknown'

df['case_type'] = df['title'].apply(classify_case_type)

# Inspect the cleaned data (optional)
print("\nCleaned Data Sample:")
print(df.head())

# Save the cleaned data to a new JSON file
df.to_json('cleaned_data.json', orient='records', indent=4)

print("\nData cleaning and preprocessing completed successfully!")
