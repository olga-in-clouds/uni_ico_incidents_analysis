"""
Data Merge Script
Purpose: Merge security incident data files from 2023 and 2024
"""

import pandas as pd
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
INPUT_FILES = {
    '2023': 'data/data-security-incidents-trends-2023.csv',
    '2024': 'data/data-security-incidents-trends-2024.csv'
}
OUTPUT_FILE = 'data/data-security-incidents-trends-2023-2024.csv'

def check_files_exist(files):
    """Verify input files exist"""
    for year, file_path in files.items():
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file for {year} not found: {file_path}")
    logger.info("All input files verified")

def merge_files(input_files, output_file):
    """Merge CSV files and save to output"""
    # Read input files
    dataframes = []
    for year, file_path in input_files.items():
        logger.info(f"Reading data for {year}")
        df = pd.read_csv(file_path)
        dataframes.append(df)
        logger.info(f"Found {len(df)} records for {year}")
    
    # Merge dataframes
    merged_df = pd.concat(dataframes, ignore_index=True)
    logger.info(f"Merged dataframe contains {len(merged_df)} records")
    
    # Save merged data
    merged_df.to_csv(output_file, index=False)
    logger.info(f"Merged data saved to {output_file}")
    
    return merged_df

def main():
    """Main execution function"""
    try:
        # Verify input files
        check_files_exist(INPUT_FILES)
        
        # Merge files
        merged_df = merge_files(INPUT_FILES, OUTPUT_FILE)
        
        # Display sample of merged data
        print("\nFirst few rows of the merged file:")
        print(merged_df.head())
        
        print(f"\nMerge complete! {len(merged_df)} total records saved to {OUTPUT_FILE}")
        
    except Exception as e:
        logger.error(f"Error merging files: {str(e)}")
        raise

if __name__ == "__main__":
    main() 