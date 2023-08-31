# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 09:59:05 2023

@author: Kristin
"""



import pandas as pd
import matplotlib.pyplot as plt
import datetime

class BMRSReport:

    def __init__(self, date, dic_ts):
        self.date = date
        self.dic_ts = dic_ts
        self.timeseries = self._build_timeseries()

    def _build_timeseries(self):
        try:
            # timeseries = pd.merge(self.dic_ts["B1770"], self.dic_ts["B1780"], on="SettlementPeriod")[["SettlementPeriod", "ImbalancePriceAmount", "Imbalance Quantity (MAW)"]]
            ts = pd.merge(self.dic_ts["B1770"], self.dic_ts["B1780"], left_on="SettlementPeriod", right_on="Settlement Period")[["SettlementPeriod","ImbalancePriceAmount","Imbalance Quantity (MAW)"]]
            ts.columns = ["Period", "Price", "Quantity"]
            ts["Period"] = ts["Period"].astype("int")
            ts["AbsQuantity"] = ts["Quantity"].apply(abs)
            return ts
        except ValueError as e:
            print(f"An error occurred with the data: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def plot_data(self):
        try:
            # Plotting both the curves simultaneously
            plt.plot(self.timeseries["Period"], self.timeseries["Price"], marker='o', color='r', label='Price')
            plt.plot(self.timeseries["Period"], self.timeseries["Quantity"], marker='o', color='b', label='Quantity')
            # Naming the x-axis, y-axis and the whole graph
            plt.xlabel("Settlement Period")
            # plt.ylabel("Magnitude")
            plt.title("Imbalance Price and Quantity")
            # Adding legend, which helps us recognize the curve according to it's color
            plt.legend()
            # To load the display window
            plt.show()
        except (ValueError, TypeError) as e:
            print(f"An error occurred while plotting: {e}")
        except RuntimeError as e:
            print(f"An error occurred during plot rendering: {e}")


    def generate_daily_imbalance_report(self):
        try:
            # Generate a message that provides the total daily imbalance cost and the daily imbalance unit rate.
            total_cost = self.timeseries["Price"].sum()
            total_abs_quantity = self.timeseries["AbsQuantity"].sum()
            daily_imbalance_rate = total_cost / total_abs_quantity
            
            # Report which Hour had the highest absolute imbalance volumes.
            max_abs_volume = self.timeseries["AbsQuantity"].max()
            period_with_max_volume = self.timeseries.iloc[self.timeseries["AbsQuantity"].idxmax(),0]
            time_with_max_volume = str(datetime.timedelta(hours=period_with_max_volume/2.0)).rsplit(':', 1)[0]

            formatted_date = datetime.datetime.strptime(self.date, "%Y-%m-%d").strftime("%d %B %Y")

            # Print the report
            print(f"Daily Impalance Report for {formatted_date}")
            print(f"Daily Imbalance Rate: {daily_imbalance_rate:2f}")
            print(f"Highest Imbalance Volume occurred at: {time_with_max_volume}")
            
        except (ValueError, TypeError) as e:
            print(f"An error occurred while generating the daily imbalance report: {e}")
        except RuntimeError as e:
            print(f"An error occurred while generating the daily imbalance report: {e}")



        # Additional analysis and visualization code can go here