# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 12:51:01 2023

@author: Kristin
"""


import unittest
from unittest.mock import patch
from data_processor.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    @patch("data_processor.data_processor.requests.get")
    def test_process_reports(self, mock_get):
        
        # TBD: Mock response data
        mock_response = mock_get.return_value
        mock_response.text = "dummy,response,data"

        # Test Data
        base_url = "https://api.bmreports.com/BMRS"
        api_key = "630m7ks51lqcvpe"
        date = "2023-08-24"
        service_type = "csv"
        reports = ["B1770", "B1780"]
    
        # Create an instance of DataProcessor
        data_processor = DataProcessor(base_url, api_key, date, service_type, reports)

        # Call process_reports method
        data_processor.process_reports()

        # Check if the expected methods were called
        self.assertTrue(mock_get.called)
        mock_get.assert_called_once_with(
            f"base_url/B1770/v1?APIKey={api_key}&Period=*&SettlementDate={date}&Period=1&ServiceType={service_type}"
        )

if __name__ == "__main__":
    unittest.main()