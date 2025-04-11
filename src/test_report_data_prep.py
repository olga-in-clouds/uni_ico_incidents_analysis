"""
Unit Tests for Report Data Preparation 
Purpose: Verify the functionality of the report_data_preperation.py 
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import logging
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from report_data_preperation import (
    validate_input_data,
    get_range_midpoint,
    normalise_column,
    calculate_severity_score,
    process_data,
    TIME_MAP,
    RANGE_MAP
)

class TestReportDataPrep(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.sample_data = pd.DataFrame({
            'BI Reference': ['BI001', 'BI001', 'BI002', 'BI003'],
            'Year': [2023, 2023, 2023, 2023],
            'Quarter': ['Q1', 'Q1', 'Q2', 'Q2'],
            'Time Taken to Report': ['Less than 24 hours', 'Less than 24 hours', '24 hours to 72 hours', 'More than 1 week'],
            'Data Type': ['Personal', 'Financial', 'Personal', 'Personal'],
            'No. Data Subjects Affected': ['1 to 9', '1 to 9', '10 to 99', 'Unknown']
        })
        
        # Create temporary files for testing
        self.input_file = "test_input.csv"
        self.output_file = "test_output.csv"

    def tearDown(self):
        """Clean up after tests"""
        # Remove temporary files
        Path(self.input_file).unlink(missing_ok=True)
        Path(self.output_file).unlink(missing_ok=True)

    def test_validate_input_data_valid(self):
        """Test validation with valid data"""
        try:
            validate_input_data(self.sample_data)
        except ValueError:
            self.fail("validate_input_data raised ValueError unexpectedly!")

    def test_validate_input_data_missing_columns(self):
        """Test validation with missing columns"""
        invalid_data = self.sample_data.drop('Year', axis=1)
        with self.assertRaises(ValueError):
            validate_input_data(invalid_data)

    def test_validate_input_data_empty(self):
        """Test validation with empty DataFrame"""
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            validate_input_data(empty_df)

    def test_validate_input_data_invalid_time(self):
        """Test validation with invalid time range"""
        invalid_data = self.sample_data.copy()
        invalid_data.loc[0, 'Time Taken to Report'] = 'Invalid Time'
        with self.assertRaises(ValueError):
            validate_input_data(invalid_data)

    def test_get_range_midpoint(self):
        """Test range midpoint calculation"""
        test_cases = [
            ('1 to 9', 5.0),
            ('10 to 99', 54.5),
            ('100 to 1k', 550.0),
            ('Unknown', np.nan),
            ('Invalid Range', np.nan)
        ]
        
        for input_range, expected_output in test_cases:
            result = get_range_midpoint(input_range)
            if pd.isna(expected_output):
                self.assertTrue(pd.isna(result))
            else:
                self.assertEqual(result, expected_output)

    def test_normalise_column(self):
        """Test column normalisation"""
        test_series = pd.Series([1, 2, 3, 4, 5])
        normalised = normalise_column(test_series, 'test')
        
        # Check normalisation bounds
        self.assertAlmostEqual(normalised.min(), 0)
        self.assertAlmostEqual(normalised.max(), 1)
        
        # Check specific values
        self.assertAlmostEqual(normalised.iloc[0], 0.0)  # First value (1) should be 0
        self.assertAlmostEqual(normalised.iloc[-1], 1.0)  # Last value (5) should be 1

    def test_normalise_column_single_value(self):
        """Test normalization with single value series"""
        test_series = pd.Series([1, 1, 1])
        result = normalise_column(test_series, 'test')
        
        # When all values are the same, normalization should return all NaN
        # because (x - min) / (max - min) = 0/0
        self.assertTrue(result.isna().all())

    def test_calculate_severity_score(self):
        """Test severity score calculation"""
        test_df = pd.DataFrame({
            'subjects_norm': [0.5, 0.7, 0.3],
            'reporting_time_norm': [0.4, 0.6, 0.2],
            'data_types_norm': [0.3, 0.5, 0.1]
        })
        
        scores = calculate_severity_score(test_df)
        
        # Check score bounds (should be between 1 and 10)
        self.assertTrue(all(scores >= 1))
        self.assertTrue(all(scores <= 10))
        
        # Test with NaN values
        test_df.loc[0, 'subjects_norm'] = np.nan
        scores_with_nan = calculate_severity_score(test_df)
        self.assertTrue(all(scores_with_nan >= 1))

    def test_process_data_integration(self):
        """Test the entire data processing pipeline"""
        # Save test data to CSV
        self.sample_data.to_csv(self.input_file, index=False)
        
        # Process the data
        process_data(self.input_file, self.output_file)
        
        # Read and verify the output
        self.assertTrue(Path(self.output_file).exists())
        result_df = pd.read_csv(self.output_file)
        
        # Check that all expected columns exist
        expected_columns = [
            'BI Reference', 'Year', 'Quarter', 'Time Taken to Report',
            'Data Type', 'No. Data Subjects Affected', 'reporting_time_hrs',
            'Incident_ID', 'subjects_num', 'data_types_per_incident',
            'subjects_norm', 'reporting_time_norm', 'data_types_norm',
            'severity_score'
        ]
        for col in expected_columns:
            self.assertIn(col, result_df.columns)
        
        # Verify data consistency
        self.assertEqual(
            len(result_df['Incident_ID'].unique()),
            len(self.sample_data['BI Reference'].unique())
        )
        
        # Check that BI001 has two data types
        bi001_data_types = result_df[
            result_df['BI Reference'] == 'BI001'
        ]['data_types_per_incident'].iloc[0]
        self.assertEqual(bi001_data_types, 2)

    def test_time_mapping(self):
        """Test time mapping values"""
        test_data = self.sample_data.copy()
        test_data['reporting_time_hrs'] = test_data['Time Taken to Report'].map(TIME_MAP)
        
        expected_mappings = {
            'Less than 24 hours': 12,
            '24 hours to 72 hours': 48,
            'More than 1 week': 192
        }
        
        for time_range, expected_hours in expected_mappings.items():
            actual_hours = test_data.loc[
                test_data['Time Taken to Report'] == time_range,
                'reporting_time_hrs'
            ].iloc[0]
            self.assertEqual(actual_hours, expected_hours)

    def test_data_type_counting(self):
        """Test counting of unique data types per incident"""
        test_data = self.sample_data.copy()
        data_type_counts = test_data.groupby('BI Reference')['Data Type'].nunique()
        
        # BI001 should have 2 unique data types (Personal and Financial)
        self.assertEqual(data_type_counts['BI001'], 2)
        # BI002 should have 1 unique data type (Personal)
        self.assertEqual(data_type_counts['BI002'], 1)

    def test_integration_cleanup(self):
        """Integration test with explicit cleanup"""
        # Save test data to CSV for the test
        self.sample_data.to_csv(self.input_file, index=False)
        
        # Process the data
        process_data(self.input_file, self.output_file)
        
        # Read and verify the output
        self.assertTrue(Path(self.output_file).exists())
        result_df = pd.read_csv(self.output_file)
        
        # Verify data consistency
        self.assertEqual(
            len(result_df['Incident_ID'].unique()),
            len(self.sample_data['BI Reference'].unique())
        )

def main():
    """Run the test suite"""
    # Configure logging to suppress log messages during tests
    logging.getLogger().setLevel(logging.ERROR)
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()