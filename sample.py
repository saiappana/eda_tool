import pandas as pd
# Import ProfileReport from ydata_profiling instead of pandas_profiling
from pandas_profiling import ProfileReport 
df = pd.read_csv("/Expanded_data_with_more_features.csv")
profile = ProfileReport(df)
profile.to_file(output_file="analysis.html")