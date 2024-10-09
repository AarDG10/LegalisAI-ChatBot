import json
import re

def clean_and_summarize(record):
    # Extract title, date, and summary from the JSON record
    title = record.get('title', '')
    date = record.get('date', '')
    summary = record.get('summary', '')

    # Step 1: Text Preprocessing
    # Clean the summary text
    summary = re.sub(r'\s+', ' ', summary).strip()  # Remove unnecessary whitespace
    summary = re.sub(r'[^\w\s,.()]', '', summary)  # Remove special characters

    # Limit the summary to 350 characters
    if len(summary) > 350:
        summary = summary[:350] + '...'  # Append ellipsis if truncated

    # Step 2: Generate a Cleaned Summary
    summary_output = {
        'title': title,
        'date': date,
        'summary': summary
    }

    return summary_output

input_file_path = '../spiders/data1.json'  # Path to your input JSON file
output_file_path = './cleaned_data.json'  # Path for the output JSON file

def summarize_json_file(input_file_path, output_file_path):
    # Load JSON data from a file
    with open(input_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    summaries = []
    for record in data:
        cleaned_summary = clean_and_summarize(record)
        summaries.append(cleaned_summary)

    # Write the summaries to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=4)

# Example usage

summarize_json_file(input_file_path, output_file_path)

print(f'Summarized data written to {output_file_path}')

