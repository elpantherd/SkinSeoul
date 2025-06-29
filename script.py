import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Load and examine the dataset
df = pd.read_excel('Mock_Skincare_Dataset.xlsx')

print("Dataset Overview:")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print("\nFirst few rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nBasic statistics:")
print(df.describe())

print("\nBrand Tier distribution:")
print(df['Brand Tier'].value_counts())

print("\nBrand distribution:")
print(df['Brand'].value_counts())

print("\nMissing values:")
print(df.isnull().sum())