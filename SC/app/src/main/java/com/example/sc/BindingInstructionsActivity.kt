package com.example.sc

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity

class BindingInstructionsActivity : AppCompatActivity() {

    private lateinit var nextButton: Button
    private lateinit var backButton: ImageView
    private var sensorName: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_binding_instructions)

        // 初始化 UI 元件
        nextButton = findViewById(R.id.next_button)
        backButton = findViewById(R.id.back_button)

        // 接收從上一頁傳遞的感測器名稱
        sensorName = intent.getStringExtra("sensorName")

        // 返回按鈕
        backButton.setOnClickListener {
            finish()
        }

        // 下一步按鈕
        nextButton.setOnClickListener {
            // 跳轉到綁定成功頁面
            val intent = Intent(this, BindingSuccessActivity::class.java)
            intent.putExtra("sensorName", sensorName) // 傳遞感測器名稱
            startActivity(intent)
        }
    }
}
