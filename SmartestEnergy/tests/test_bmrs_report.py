# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 12:51:01 2023

@author: Kristin
"""

import unittest
import pandas as pd
import datetime
from reports.bmrs_report import BMRSReport

class TestBMRSReport(unittest.TestCase):
    
    def test_bmrs_report(self):
        # Create sample data for testing
        dic_ts = {
            "B1770": pd.DataFrame({
                "SettlementPeriod": [1, 2, 3],
                "ImbalancePriceAmount": [10.0, 12.0, 15.0],
                "Imbalance Quantity (MAW)": [-20, -25, -30]
            }),
            "B1780": pd.DataFrame({
                "SettlementPeriod": [1, 2, 3],
                "ImbalancePriceAmount": [8.0, 10.0, 9.5],
                "Imbalance Quantity (MAW)": [15, 20, 22]
            })
        }

        bmrs_report = BMRSReport("2023-08-23", dic_ts)
        
        # Suppress plot rendering in tests
        bmrs_report._plot = lambda: None

        # Generate the plot
        bmrs_report.plot_data()

        # TBD: add more specific assertions
        # eg check if certain plot elements are present
        # or if the title matches



class TestGenerateDailyImbalanceReport(unittest.TestCase):

    def setUp(self):
        # Create sample timeseries data
        data = {
            "SettlementPeriod": [1, 2, 3],
            "Price": [10.0, 12.0, 15.0],
            "AbsQuantity": [20, 25, 30]
        }
        self.timeseries = pd.DataFrame(data)
        self.date = "2023-08-24"
        self.bmrs_report = BMRSReport(self.date, self.timeseries)

    def test_generate_daily_imbalance_report(self):
        # Expected results
        expected_daily_imbalance_rate = (10.0 + 12.0 + 15.0) / (20 + 25 + 30)
        expected_time_with_max_volume = "0:30"
        formatted_date = datetime.datetime.strptime(self.date, "%Y-%m-%d").strftime("%d %B %Y")

        # Redirect print output for testing
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the method to generate the report
        self.bmrs_report.generate_daily_imbalance_report()

        # Restore print output
        sys.stdout = sys.__stdout__

        # Get printed output
        printed_output = captured_output.getvalue().strip()

        # Assert that the printed output matches the expected format
        self.assertIn(f"Daily Impalance Report for {formatted_date}", printed_output)
        self.assertIn(f"Daily Imbalance Rate: {expected_daily_imbalance_rate:.2f}", printed_output)
        self.assertIn(f"Highest Imbalance Volume occurred at: {expected_time_with_max_volume}", printed_output)



if __name__ == "__main__":
    unittest.main()




