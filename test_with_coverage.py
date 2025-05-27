import unittest
import coverage
import pandas as pd
import os
from financial_statement import save_dataframe


class TestSaveDataFrame(unittest.TestCase):
    def test_save_data_frame_success(self):
        """If there is data, saves the files successfully."""
        df = pd.DataFrame({"Months": ["2024-01"], "Balance_cleaned": [1000]})
        result = save_dataframe(df, "test.csv", "test.json")
        self.assertTrue(result)  # Check if result is True
        self.assertTrue(os.path.exists("test.csv"))  # Does the CSV file exist?
        self.assertTrue(os.path.exists("test.json"))  # Does the JSON file exist?
        # Cleaning
        os.remove("test.csv")
        os.remove("test.json")

    def test_save_data_frame_empty(self):
        """If DataFrame is empty, won't save the files"""
        df = pd.DataFrame()  # Empty DataFrame
        result = save_dataframe(df, "test.csv", "test.json")
        self.assertFalse(result)  # Check if result is False
        self.assertFalse(os.path.exists("test.csv"))
        self.assertFalse(os.path.exists("test.json"))

    def test_permission_error(self):
        df = pd.DataFrame({"Date": ["2022-01-01"], "Balance": [1000]})
        restricted_dir = "/root"  # Write-protected (Windows)
        invalid_csv_path = os.path.join(restricted_dir, "test.csv")
        invalid_json_path = os.path.join(restricted_dir, "test.json")
        # Test if finish with PermissionError
        result = save_dataframe(df, invalid_csv_path, invalid_json_path)
        # Test: False when cannot save
        self.assertFalse(result)


# Launch Code Coverage
cov = coverage.Coverage()
cov.start()

# Run tests
loader = unittest.TestLoader()
suite = loader.discover(start_dir="financial_statements")  # Folder of test file
runner = unittest.TextTestRunner()
runner.run(suite)

# Stop and Generate report
cov.stop()
cov.save()

# Print result
cov.report()
cov.html_report(directory="coverage_report")  # Generate HTML report


if __name__ == "__main__":
    unittest.main()

