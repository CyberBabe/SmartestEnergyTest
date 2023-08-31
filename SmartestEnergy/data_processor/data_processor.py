# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 09:47:50 2023

@author: Kristin
"""


import requests
import pandas as pd
from pathlib import Path
import os


class DataProcessor:

    def __init__(self, base_url, api_key, date, service_type, reports):
        self.base_url = base_url
        self.api_key = api_key
        self.date = date
        self.service_type = service_type
        self.reports = reports
        self.dic_ts = {}

    def call_api(self, report, period):
        try:
            url = f"{self.base_url}/{report}/v1?APIKey={self.api_key}&Period=*&SettlementDate={self.date}&Period={period}&ServiceType={self.service_type}"
            res = requests.get(url)
            res.raise_for_status()
            return res.text
        except requests.RequestException as e:
            print(f"Failed to fetch data for period {period}: {e}")
            return None

    def get_data_from_api(self):
        for report in self.reports:
            ts = pd.DataFrame()
            data_directory = Path.cwd() / "data_processor/data"
            data_directory.mkdir(parents=True, exist_ok=True)
            
            for i in range(1, 51):
                period = str(i)
                try:
                    data = self.call_api(report, period)
                    if data:
                        # report = "B1770"
                        # period = 3
                        fname = os.path.join(data_directory, f'{report}_data_{period}.csv')
                        # fname = f'{report}_data_{period}.csv'
                        # print(fname)
                        with open(fname, "w") as f:
                            f.write(data)
                        data = pd.read_csv(fname, skiprows=4)
                        #(Path.cwd() / fname).write_text(data)
                        #data = pd.read_csv(f'./{fname}', skiprows=4)
                        ts = pd.concat([ts, data[data.iloc[:, 0] != '<EOF>']], axis=0)
                except:
                    print(f"{period} failed to load")
                    
            self.dic_ts[report] = ts
            # print(ts.shape)
            # ts.to_csv(f'./{report}_data.csv')
            ts.to_csv(os.path.join(data_directory, f'./{report}_data.csv'))
            
    def get_data_from_file(self, path=""):
        if path == "":
            path = Path.cwd() / "data_processor/data"
        try:
            for report in self.reports:
                ts = pd.read_csv(os.path.join(path, f'./{report}_data.csv'))
                self.dic_ts[report] = ts
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print(f"An error occurred: {e}")
