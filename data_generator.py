import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataGenerator:
    '''Generate sample financial data for testing'''
    
    @staticmethod
    def generate_financial_data(days=365):
        '''Generate comprehensive financial dataset'''
        
        np.random.seed(42)
        
        # Date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        n = len(dates)
        
        # Simulate stock price movement
        price = 100
        prices = []
        for i in range(n):
            price = price * (1 + np.random.normal(0.001, 0.02))
            prices.append(max(price, 10))  # Prevent negative prices
        
        # Create comprehensive dataset
        df = pd.DataFrame({
            'Date': dates,
            'Open': [p * np.random.uniform(0.98, 1.02) for p in prices],
            'High': [p * np.random.uniform(1.00, 1.05) for p in prices],
            'Low': [p * np.random.uniform(0.95, 1.00) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000000, 10000000, n),
            'Revenue': np.random.uniform(50000, 200000, n),
            'Expenses': np.random.uniform(30000, 150000, n),
            'Sector': np.random.choice(['Technology', 'Finance', 'Healthcare', 'Energy'], n),
            'Market_Cap': np.random.uniform(1e9, 1e11, n),
            'PE_Ratio': np.random.uniform(10, 50, n),
            'ROI': np.random.uniform(-10, 30, n),
        })
        
        # Ensure High >= max(Open, Close) and Low <= min(Open, Close)
        df['High'] = df[['High', 'Open', 'Close']].max(axis=1)
        df['Low'] = df[['Low', 'Open', 'Close']].min(axis=1)
        
        # Derived columns
        df['Profit'] = df['Revenue'] - df['Expenses']
        df['Returns'] = df['Close'].pct_change() * 100
        df['Month'] = df['Date'].dt.strftime('%Y-%m')
        df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
        df['Year'] = df['Date'].dt.year
        df['Day_of_Week'] = df['Date'].dt.day_name()
        
        # Fill NaN in Returns
        df['Returns'] = df['Returns'].fillna(0)
        
        return df
    
    @staticmethod
    def get_column_info(df):
        '''Get information about each column'''
        info = {}
        for col in df.columns:
            info[col] = {
                'type': str(df[col].dtype),
                'is_numeric': pd.api.types.is_numeric_dtype(df[col]),
                'is_datetime': pd.api.types.is_datetime64_any_dtype(df[col]),
                'unique_values': int(df[col].nunique()),
                'has_nulls': bool(df[col].isnull().any())
            }
        return info