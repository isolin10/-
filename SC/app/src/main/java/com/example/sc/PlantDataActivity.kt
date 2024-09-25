package com.example.sc

import android.os.Bundle
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.TableLayout
import android.widget.TableRow
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import com.google.firebase.FirebaseApp
import com.google.firebase.FirebaseOptions
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.FirebaseFirestoreSettings
import java.io.FileInputStream

class PlantDataActivity : AppCompatActivity() {

    private lateinit var plantImage: ImageView
    private lateinit var plantName: TextView
    private lateinit var dataTable: TableLayout
    private lateinit var backButton: ImageButton

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_plant_data)

        // 初始化UI元件
        plantImage = findViewById(R.id.plant_image)
        plantName = findViewById(R.id.plant_name)
        dataTable = findViewById(R.id.data_table)
        backButton = findViewById(R.id.back_button)

        // 取得從前一頁傳來的資料
        val subject = intent.getStringExtra("subject")
        val imageUrl = intent.getStringExtra("imageUrl")

        // 設定植物名稱和圖片
        plantName.text = subject ?: "無資料"
        imageUrl?.let {
            Glide.with(this).load(it).into(plantImage)
        }

        // 監聽返回按鈕，按下後返回主頁
        backButton.setOnClickListener {
            finish()
        }
        val db = FirebaseFirestore.getInstance()
        val settings = FirebaseFirestoreSettings.Builder()
            .setPersistenceEnabled(false)  // 禁用本地缓存
            .build()
        db.firestoreSettings = settings

        // 初始化第二個 FirebaseApp
        initializeSecondFirebaseApp()

        // 從第二個 Firebase 專案中取得數據
        fetchPlantDataFromFirestore()
    }

    private fun initializeSecondFirebaseApp() {
        // 初始化第二個 FirebaseApp
        val options = FirebaseOptions.Builder()
            .setProjectId("group9-b1978")
            .setApplicationId("1:722627005346:android:1b08072db104a606f240fb")  // 对应你的应用 ID
            .setApiKey("AIzaSyBBWhFEtU6dTpdtS5heW5zLBd_5Y7I0kRs")
            .setDatabaseUrl("https://group9-b1978.firebaseio.com/")  // 如果使用 Firestore，可能不需要 Database URL
            .setStorageBucket("group9-b1978.appspot.com")
            .build()

        FirebaseApp.initializeApp(this /* Context */, options, "secondProject")
    }

    private fun fetchPlantDataFromFirestore() {
        // 取得第二個 FirebaseApp 實例
        val secondApp = FirebaseApp.getInstance("secondProject")
        val db = FirebaseFirestore.getInstance(secondApp)

        // 從第二個Firebase專案的資料庫取得數據
        db.collection("soildData").document("all_data")
            .get()
            .addOnSuccessListener { document ->
                if (document.exists()) {
                    val data = document.get("data") as List<Map<String, Any>>?
                    if (data != null && data.isNotEmpty()) {
                        val limitedData = data.take(4)
                        for (entry in limitedData) {
                            val tableRow = TableRow(this)

                            val dateText = TextView(this)
                            dateText.text = entry["date"].toString()

                            val tempText = TextView(this)
                            tempText.text = entry["temp"].toString()

                            val humdText = TextView(this)
                            humdText.text = entry["humd"].toString()

                            val lightText = TextView(this)
                            lightText.text = entry["light"].toString()

                            val phText = TextView(this)
                            phText.text = entry["ph"].toString()

                            val saltText = TextView(this)
                            saltText.text = entry["salt"].toString()

                            // 將這些TextView添加到Row裡
                            tableRow.addView(dateText)
                            tableRow.addView(tempText)
                            tableRow.addView(humdText)
                            tableRow.addView(lightText)
                            tableRow.addView(phText)
                            tableRow.addView(saltText)

                            // 把Row加到表格中
                            dataTable.addView(tableRow)
                        }
                    } else {
                        Toast.makeText(this, "沒有找到數據", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(this, "文檔不存在", Toast.LENGTH_SHORT).show()
                }
            }
            .addOnFailureListener { exception ->
                // 處理錯誤
                Toast.makeText(this, "讀取資料失敗: ${exception.message}", Toast.LENGTH_LONG).show()
            }
    }
}
