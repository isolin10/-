import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# 初始化 Firebase 應用程式
cred = credentials.Certificate("path/to/firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 將預測結果轉換為Firebase格式
result_dict = {
    'day': ['day 1', 'day 2', 'day 3', ..., 'day N'],
    'humidity': [predicted_values[0], predicted_values[1], predicted_values[2], ..., predicted_values[N-1]],
    'nitrogen': [predicted_values[0], predicted_values[1], predicted_values[2], ..., predicted_values[N-1]],
    'lithium': [predicted_values[0], predicted_values[1], predicted_values[2], ..., predicted_values[N-1]],
    'potassium': [predicted_values[0], predicted_values[1], predicted_values[2], ..., predicted_values[N-1]]
}

result_df = pd.DataFrame(result_dict)
result_data = result_df.to_dict(orient='records')

# 指定要上傳到的Firebase集合的路徑
result_collection_ref = db.collection('your-result-collection')

# 將預測結果上傳到Firebase
for day_data in result_data:
    result_collection_ref.add(day_data)
