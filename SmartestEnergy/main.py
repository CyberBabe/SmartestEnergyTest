# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 09:44:56 2023

@author: Kristin
"""

from data_processor.data_processor import DataProcessor
from reports.bmrs_report import BMRSReport

import pandas as pd
import matplotlib.pyplot as plt

def main(call_api=True):

    base_url = "https://api.bmreports.com/BMRS"
    api_key = "630m7ks51lqcvpe"     # This needs to be handled better
    date = "2023-08-24"
    service_type = "csv"
    reports = ["B1770", "B1780"]

    data_processor = DataProcessor(base_url, api_key, date, service_type, reports)

    if call_api:
        # Generate data by calling the api
        data_processor.get_data_from_api()
    else:
        # Get the data from previously saved files
        data_processor.get_data_from_file()

    dic_ts = data_processor.dic_ts

    bmrs_report = BMRSReport(date, dic_ts)
    bmrs_report.plot_data()
    bmrs_report.generate_daily_imbalance_report()



if __name__ == "__main__":
    # Run with parameter False to use data previously downloaded
    main(False)
