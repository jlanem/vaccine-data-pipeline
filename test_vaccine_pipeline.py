import os
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from vaccine_pipeline import fetch_vaccine_data, plot_vaccine_data, save_to_csv


class TestVaccinePipeline(unittest.TestCase):

    @patch("requests.get")
    def test_fetch_vaccine_data_success(self, mock_get):
        """Test fetching vaccine data with a valid response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"country": "USA", "timeline": {"2024-03-23": 500000000}},
            {"country": "UK", "timeline": {"2024-03-23": 100000000}},
        ]
        mock_get.return_value = mock_response

        data = fetch_vaccine_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["country"], "USA")
        self.assertEqual(data[0]["vaccines_administered"], 500000000)

    @patch("requests.get")
    def test_fetch_vaccine_data_network_error(self, mock_get):
        """Test handling of network errors"""
        mock_get.side_effect = Exception("Network error")
        data = fetch_vaccine_data()
        self.assertIn("error", data)
        self.assertTrue("Network error" in data["error"])

    def test_save_to_csv(self):
        """Test saving vaccine data to CSV"""
        test_data = [
            {"country": "USA", "vaccines_administered": 500000000},
            {"country": "UK", "vaccines_administered": 100000000},
        ]
        filename = "test_vaccine_coverage.csv"
        save_to_csv(test_data, filename)

        self.assertTrue(os.path.exists(filename))

        df = pd.read_csv(filename)
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]["country"], "USA")
        self.assertEqual(df.iloc[0]["vaccines_administered"], 500000000)

        os.remove(filename)  # Cleanup

    def test_plot_vaccine_data(self):
        """Test if plot_vaccine_data runs without errors"""
        test_data = [
            {"country": "USA", "vaccines_administered": 500000000},
            {"country": "UK", "vaccines_administered": 100000000},
        ]
        try:
            plot_vaccine_data(test_data)
        except Exception as e:
            self.fail(f"plot_vaccine_data() raised an error: {e}")


if __name__ == "__main__":
    unittest.main()
