import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# 下載 Firebase 密鑰 JSON 檔案並將其放在您的專案資料夾中
# 在 Firebase 控制台中，進入您的專案 -> 項目設定 -> 服務帳戶 -> 產生私密金鑰
cred = credentials.Certificate("path/to/firebase-key.json")

# 初始化 Firebase 應用程式
firebase_admin.initialize_app(cred)

# 初始化 Firestore 客戶端
db = firestore.client()

# 指定您的 Firebase 集合的路徑
collection_ref = db.collection('plant-data')

# 擷取集合中的所有文件
docs = collection_ref.stream()

# 創建一個空的 DataFrame 來存儲 Firebase 數據
data = pd.DataFrame(columns=['date', 'temp', 'humd', 'salt', 'ec', 'ph', 'n', 'p', 'l', 'light'])

# 遍歷每個文件並將數據添加到 DataFrame 中
for doc in docs:
    doc_data = doc.to_dict()
    doc_id = doc.id
    date = doc_data['date']
    temp = doc_data['temp']
    humd = doc_data['humd']
    salt = doc_data['salt']
    ec = doc_data['ec']
    ph = doc_data['ph']
    n = doc_data['n']
    p = doc_data['p']
    l = doc_data['l']
    light = doc_data['light']
    
    data = data.append({'date': date, 'temp': temp, 'humd': humd, 'salt': salt, 'ec': ec, 'ph': ph, 'n': n, 'p': p, 'l': l, 'light': light}, ignore_index=True)

# 打印抓取的資料
print(data.head())

# 將數據保存到 CSV 檔案中
data.to_csv('plant_data.csv', index=False)
