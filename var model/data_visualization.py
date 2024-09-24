#負責資料的視覺化展示。
import pandas as pd 
import matplotlib.pyplot as plt

def plot_data(df: pd.DataFrame):
    """
    繪製資料的時間序列圖。
    :param df: 資料 DataFrame
    """
    df.plot(subplots=True, figsize=(12, 10))
    plt.show()

