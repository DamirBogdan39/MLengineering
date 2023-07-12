import pandas as pd
import os 

def split_dataframe(df, file1, file2):


    num_columns = df.shape[1]
    
    half_columns = num_columns // 2
    
    df1 = df.iloc[:, :half_columns]
    
    df2 = df.iloc[:, half_columns:]
    
    # Save the two DataFrames to separate files
    
    df1.to_csv(file1, index=False)
    
    df2.to_parquet(file2, index=False)
    
    print("DataFrames saved successfully!")


current_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(current_dir, '../../data/raw/raw.csv')


# Split the data frame

split_dataframe(pd.read_csv(file_path), '../../data/raw/source_1.csv', '../../data/raw/source_2.parquet')
