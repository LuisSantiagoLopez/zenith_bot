import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

# Load the DataFrame from the CSV file
df = pd.read_csv('combined_dataset.csv')

# Filter out rows without a website
df_with_websites = df.dropna(subset=['website']).reset_index(drop=True)

# Function to scrape content and extract emails
def scrape_website(url):
    try:
        print(f"Scraping website: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all text content
        content = soup.get_text(separator=' ', strip=True)
        
        # Find all email addresses
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", content)
        
        return content, emails
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None, None

# Initialize new columns
df_with_websites['content'] = ''
df_with_websites['Emails'] = ''

# Process the first 10 websites and update the DataFrame
for index, row in df_with_websites.iterrows():
    print(f"Processing row {index + 1}/{len(df_with_websites)}: {row['website']}")
    content, emails = scrape_website(row['website'])
    if content and emails:
        df_with_websites.at[index, 'content'] = content
        df_with_websites.at[index, 'Emails'] = ', '.join(emails)
        print(f"Content and emails extracted for {row['website']}")
    else:
        df_with_websites.at[index, 'content'] = 'Error scraping content'
        df_with_websites.at[index, 'Emails'] = 'Error extracting emails'
        print(f"Failed to extract content or emails for {row['website']}")
    time.sleep(1)  # To prevent overwhelming the server

# Debugging: Show the first 10 rows after scraping
print("First 10 rows after scraping:")
print(df_with_websites.head(10))

# Create DataFrames for instances with both content and email, and with missing content or email
df_complete = df_with_websites[(df_with_websites['content'] != 'Error scraping content') & (df_with_websites['Emails'] != 'Error extracting emails') & (df_with_websites['Emails'] != '')]
df_incomplete = df_with_websites[~df_with_websites.index.isin(df_complete.index)]

# Debugging: Show the counts of each DataFrame
print(f"Number of complete rows: {len(df_complete)}")
print(f"Number of incomplete rows: {len(df_incomplete)}")

# Save the DataFrames to new CSV files
output_file_complete = 'complete_dataset.csv'
output_file_incomplete = 'incomplete_dataset.csv'
df_complete.to_csv(output_file_complete, index=False, escapechar='\\')
df_incomplete.to_csv(output_file_incomplete, index=False, escapechar='\\')
print(f"Scraping complete. Complete DataFrame saved as '{output_file_complete}'. Incomplete DataFrame saved as '{output_file_incomplete}'.")
