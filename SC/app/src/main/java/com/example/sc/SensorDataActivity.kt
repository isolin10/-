package com.example.sc
import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.sc.R

class SensorDataActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sensor_data)

        // 取得感測器名稱
        val sensorName = intent.getStringExtra("sensor_name")
        val sensorNameTextView = findViewById<TextView>(R.id.sensor_name)
        sensorNameTextView.text = sensorName

        // TODO: 加載和顯示感測器的相關數據
    }
}
