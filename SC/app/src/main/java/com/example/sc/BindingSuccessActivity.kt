package com.example.sc

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class BindingSuccessActivity : AppCompatActivity() {

    private lateinit var confirmButton: Button
    private var sensorName: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_binding_success)

        // 初始化 UI 元件
        confirmButton = findViewById(R.id.confirm_button)

        // 接收從上一頁傳遞的感測器名稱
        sensorName = intent.getStringExtra("sensorName")

        // 點擊確認按鈕返回感測器頁面
        confirmButton.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java) // 假設回到主頁的 SensorFragment
            intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_NEW_TASK
            startActivity(intent)
            finish()
        }
    }
}
