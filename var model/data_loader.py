#負責資料的讀取和預處理。
import pandas as pd

def load_data(file_path: str):
    """
    從 CSV 檔案中讀取資料，並將日期設為索引。
    :param file_path: CSV 檔案路徑
    :return: 預處理後的 DataFrame
    """
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = df.dropna()  # 移除缺失值
    return df

def diff_data(df: pd.DataFrame):
    """
    對資料進行差分處理，保持穩定性。
    :param df: 原始資料
    :return: 差分後的資料
    """
    return df.diff().dropna()
