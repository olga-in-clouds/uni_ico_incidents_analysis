"""
Security Incidents Data Preparation Script
Version: 1.0

Purpose: Enhance security incident data with calculated metrics including:
- Reporting time in hours
- Impacted people numbers
- Data type counts
- Severity scores

Input: data-security-incidents-trends-2023-2024.csv
Output: data-security-incidents-trends-2023-2024_enhanced.csv
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple, Union
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants and Configuration
# Time taken to report in hours
TIME_MAP: Dict[str, int] = {
    'Less than 24 hours': 12,
    '24 hours to 72 hours': 48,
    '72 hours to 1 week': 160,
    'More than 1 week': 192
}

# Range map for impacted people numbers
RANGE_MAP: Dict[str, Tuple[Union[int, float], Union[int, float]]] = {
    '1 to 9': (1, 9),
    '10 to 99': (10, 99),
    '100 to 1k': (100, 1000),
    '1k to 10k': (1000, 10000),
    '10k to 100k': (10000, 100000),
    '100k and above': (100000, 1000000),
    'Unknown': (np.nan, np.nan)
}

# Severity weights for the severity score
SEVERITY_WEIGHTS: Dict[str, float] = {
    'subjects': 0.5,
    'reporting_time': 0.3,
    'data_types': 0.2
}

# Required columns for validation
REQUIRED_COLUMNS = [
    'BI Reference', 
    'Year', 
    'Quarter', 
    'Time Taken to Report', 
    'Data Type',
    'No. Data Subjects Affected'
]   

def validate_input_data(df: pd.DataFrame) -> None:
    """
    Validate input DataFrame structure and content.
    Raises ValueError if validation fails.
    """
    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("Input DataFrame is empty")

    # Check required columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Validate time ranges, excluding NaN values
    non_null_times = df['Time Taken to Report'].dropna()
    invalid_times = non_null_times[~non_null_times.str.strip().isin(TIME_MAP.keys())]
    if not invalid_times.empty:
        raise ValueError(f"Invalid time ranges found: {invalid_times.unique()}")

    # Log warning about NaN values if present
    nan_count = df['Time Taken to Report'].isna().sum()
    if nan_count > 0:
        logger.warning(f"Found {nan_count} NaN values in 'Time Taken to Report' column")

def get_range_midpoint(value: str) -> float:
    """Return the midpoint of the affected range."""
    if value in RANGE_MAP and not pd.isna(RANGE_MAP[value][0]):
        low, high = RANGE_MAP[value]
        return (low + high) / 2
    return np.nan


def normalise_column(series: pd.Series, name: str) -> pd.Series:
    """Normalize a column to range 0-1."""
    try:
        normalised = (series - series.min()) / (series.max() - series.min())
        return normalised
    except Exception as e:
        logger.error(f"Error normalising {name}: {str(e)}")
        raise

def calculate_severity_score(df: pd.DataFrame) -> pd.Series:
    """Calculate severity score from normalised components."""
    return round(1 + 9 * (
        df['subjects_norm'].fillna(0) * SEVERITY_WEIGHTS['subjects'] +
        df['reporting_time_norm'].fillna(0) * SEVERITY_WEIGHTS['reporting_time'] +
        df['data_types_norm'].fillna(0) * SEVERITY_WEIGHTS['data_types']
    ), 0)

def process_data(input_file: str, output_file: str) -> None:
    """Main data processing function."""
    try:
        # Read and validate input
        logger.info(f"Reading input file: {input_file}")
        df = pd.read_csv(input_file)
        validate_input_data(df)

        # Clean whitespace
        df['No. Data Subjects Affected'] = df['No. Data Subjects Affected'].str.strip()
        df['Time Taken to Report'] = df['Time Taken to Report'].str.strip()

        # Map reporting time to hours
        logger.info("Mapping reporting times to hours")
        df['reporting_time_hrs'] = df['Time Taken to Report'].map(TIME_MAP)

        # Create Incident_ID
        df['Incident_ID'] = df['BI Reference'] + '_' + df['Year'].astype(str) + '_' + df['Quarter']

        # Generate subject numbers
        logger.info("Assigning subject numbers using range midpoints")
        incident_subjects = df[['Incident_ID', 'No. Data Subjects Affected']].drop_duplicates()
        incident_subjects['subjects_num'] = incident_subjects['No. Data Subjects Affected'].apply(get_range_midpoint)
        df = df.merge(incident_subjects[['Incident_ID', 'subjects_num']], on='Incident_ID', how='left')


        # Count data types per incident
        logger.info("Calculating data types per incident")
        # Calculate unique data types per incident and merge it back
        data_type_counts = df.groupby('Incident_ID')['Data Type'].nunique().reset_index()
        data_type_counts.rename(columns={'Data Type': 'data_types_per_incident'}, inplace=True)
        df = df.merge(data_type_counts, on='Incident_ID', how='left')


        # Calculate normalized components
        logger.info("Calculating severity scores")
        df['subjects_norm'] = normalise_column(df['subjects_num'], 'subjects')
        df['reporting_time_norm'] = normalise_column(df['reporting_time_hrs'], 'reporting_time')
        df['data_types_norm'] = normalise_column(df['data_types_per_incident'], 'data_types')

        # Calculate severity score
        df['severity_score'] = calculate_severity_score(df)

        # Save enhanced data
        logger.info(f"Saving enhanced data to: {output_file}")
        df.to_csv(output_file, index=False)

        # Verify consistency
        check = df.groupby('Incident_ID')[
            ['subjects_norm', 'reporting_time_norm', 'data_types_norm', 'severity_score']
        ].nunique()
        
        inconsistencies = check[(check > 1).any(axis=1)]
        if not inconsistencies.empty:
            logger.warning("⚠️ Inconsistencies found in the following Incident_IDs:")
            logger.warning(inconsistencies)
        else:
            logger.info("✅ All Incident_IDs have consistent values")

    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise

def main():
    """Main execution function."""
    input_file = "data/data-security-incidents-trends-2023-2024.csv"
    output_file = "data/data-security-incidents-trends-2023-2024_enhanced.csv"

    try:
        process_data(input_file, output_file)
        logger.info("✅ Processing completed successfully")
    except Exception as e:
        logger.error(f"❌ Processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()