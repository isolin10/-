package com.example.sc

import android.graphics.Color
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter
import com.github.mikephil.charting.formatter.ValueFormatter
import com.google.firebase.FirebaseApp
import com.google.firebase.FirebaseOptions
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.FirebaseFirestoreSettings
import java.text.SimpleDateFormat
import java.util.*

class PlantDataActivity : AppCompatActivity() {

    private lateinit var plantImage: ImageView
    private lateinit var plantName: TextView
    private lateinit var dataTable: TableLayout
    private lateinit var backButton: ImageButton
    private lateinit var lineChart: LineChart

    private var chartData = mutableListOf<Entry>()
    private var dataList = mutableListOf<Map<String, Any>>()  // 儲存所有取得的資料
    private val dateFormat = SimpleDateFormat("MM/dd", Locale.getDefault()) // 日期格式

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_plant_data)

        // 初始化 UI 元件
        plantImage = findViewById(R.id.plant_image)
        plantName = findViewById(R.id.plant_name)
        dataTable = findViewById(R.id.data_table)
        backButton = findViewById(R.id.back_button)
        lineChart = findViewById(R.id.line_chart)

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

        // 初始化 Firebase 和設置 Firebase Firestore
        initializeFirebaseAndFetchData()

        // 設置按鈕的點擊事件
        setupButtonListeners()
    }

    private fun initializeFirebaseAndFetchData() {
        val options = FirebaseOptions.Builder()
            .setProjectId("group9-b1978")
            .setApplicationId("1:722627005346:android:1b08072db104a606f240fb")
            .setApiKey("AIzaSyBBWhFEtU6dTpdtS5heW5zLBd_5Y7I0kRs")
            .setDatabaseUrl("https://group9-b1978.firebaseio.com/")
            .setStorageBucket("group9-b1978.appspot.com")
            .build()

        // 初始化 FirebaseApp
        FirebaseApp.initializeApp(this, options, "secondProject")
        val secondApp = FirebaseApp.getInstance("secondProject")
        val db = FirebaseFirestore.getInstance(secondApp)

        val settings = FirebaseFirestoreSettings.Builder()
            .setPersistenceEnabled(false)
            .build()
        db.firestoreSettings = settings

        // 從第二個 Firebase 專案的資料庫取得數據
        db.collection("soildData").document("all_data")
            .get()
            .addOnSuccessListener { document ->
                if (document.exists()) {
                    val data = document.get("data") as List<Map<String, Any>>?
                    if (data != null && data.isNotEmpty()) {
                        val limitedData = data.take(4)  // 只取前四筆資料
                        dataList.addAll(limitedData)
                        updateTable(limitedData)
                        updateChart("temp")  // 預設顯示溫度
                    } else {
                        Toast.makeText(this, "沒有找到數據", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(this, "文檔不存在", Toast.LENGTH_SHORT).show()
                }
            }
            .addOnFailureListener { exception ->
                Toast.makeText(this, "讀取資料失敗: ${exception.message}", Toast.LENGTH_LONG).show()
            }
    }

    private fun updateTable(data: List<Map<String, Any>>) {
        for (entry in data) {
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

            // 將這些 TextView 添加到 Row 裡
            tableRow.addView(dateText)
            tableRow.addView(tempText)
            tableRow.addView(humdText)
            tableRow.addView(lightText)
            tableRow.addView(phText)
            tableRow.addView(saltText)

            // 把 Row 加到表格中
            dataTable.addView(tableRow)
        }
    }

    private fun setupButtonListeners() {
        findViewById<Button>(R.id.button_temp).setOnClickListener { updateChart("temp") }
        findViewById<Button>(R.id.button_humd).setOnClickListener { updateChart("humd") }
        findViewById<Button>(R.id.button_ph).setOnClickListener { updateChart("ph") }
        findViewById<Button>(R.id.button_light).setOnClickListener { updateChart("light") }
        findViewById<Button>(R.id.button_salt).setOnClickListener { updateChart("salt") } // 新增鹽度按鈕
    }

    // 將日期字串轉換為浮點數（時間戳），供圖表的 X 軸使用
    private fun parseDateToFloat(dateString: String): Float {
        return try {
            // 使用正確的日期格式解析日期字串
            val sdf = SimpleDateFormat("MM/dd/yyyy hh:mm:ss a", Locale.getDefault())
            val date = sdf.parse(dateString)
            // 返回日期時間戳（毫秒）轉換為浮點數，除以1000以取得秒級別的時間戳（減少浮點數精度問題）
            date?.time?.toFloat()?.div(1000) ?: 0f
        } catch (e: Exception) {
            e.printStackTrace()
            0f  // 若解析失敗，返回 0
        }
    }

    private fun updateChart(type: String) {
        // 清空現有的圖表資料
        chartData.clear()
        val dateLabels = mutableListOf<String>()  // 儲存所有日期標籤

        // 根據類型篩選資料並更新折線圖
        for ((index, entry) in dataList.withIndex()) {
            val dateString = entry["date"].toString()
            val yValue = (entry[type] as? Number)?.toFloat() ?: 0f
            chartData.add(Entry(index.toFloat(), yValue))  // 使用索引作為 X 軸的值
            dateLabels.add(dateString)  // 加入日期標籤
        }

        val lineDataSet = LineDataSet(chartData, type).apply {
            color = Color.RED
            valueTextColor = Color.BLACK
            lineWidth = 2f
            circleRadius = 4f
        }

        // 設置 X 軸格式化方式以顯示日期
        val xAxis = lineChart.xAxis
        xAxis.valueFormatter = IndexAxisValueFormatter(dateLabels)  // 使用索引標籤顯示
        xAxis.granularity = 1f  // 設置最小間隔，防止重複標籤
        xAxis.labelRotationAngle = -45f  // 設置標籤旋轉角度，防止重疊

        val lineData = LineData(lineDataSet)
        lineChart.data = lineData
        lineChart.invalidate()  // 刷新圖表
    }


    // 自定義 X 軸的標籤格式化
    class DateValueFormatter : ValueFormatter() {
        private val dateFormat = SimpleDateFormat("MM/dd HH:mm", Locale.getDefault())  // 顯示為 "MM/dd HH:mm" 格式

        override fun getFormattedValue(value: Float): String {
            // 由於時間戳已經除以1000，需要乘回來以得到毫秒級別的時間
            return dateFormat.format(Date((value * 1000).toLong()))  // 將浮點數轉換為日期格式顯示
        }
    }



}
