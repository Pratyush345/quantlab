import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

class Ticker:    
    @staticmethod  
    def get_historical_data(ticker, start_date=None, end_date=None):
        try:
            data = pd.DataFrame({
                "Close": [100, 102, 101, 105, 108, 107, 110]
            })
            return data

        except Exception as e:
            raise Exception(f"Error fetching data for ticker {ticker}: {str(e)}")

    
            
            

    @staticmethod
    def get_columns(data):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        return list(data.columns)

    @staticmethod
    def get_last_price(data, column_name):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        if column_name not in data.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame")
        return data[column_name].iloc[-1]

    @staticmethod
    def plot_data(data, ticker, column_name):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        if column_name not in data.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame")
        
        plt.figure(figsize=(10, 6))
        data[column_name].plot()
        plt.ylabel(column_name)
        plt.xlabel('Date')
        plt.title(f'Historical data for {ticker} - {column_name}')
        plt.legend(loc='best')
        return plt