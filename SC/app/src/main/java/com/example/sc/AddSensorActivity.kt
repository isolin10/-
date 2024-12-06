package com.example.sc
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.sc.BindingInstructionsActivity
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase

class AddSensorActivity : AppCompatActivity() {

    private lateinit var sensorNameInput: EditText
    private lateinit var cropTypeInput: EditText
    private lateinit var nextButton: Button
    private lateinit var backButton: ImageView
    private lateinit var database: DatabaseReference  // Realtime Database 參考

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_add_sensor)

        // 初始化 UI 元件
        sensorNameInput = findViewById(R.id.sensor_name_input)
        cropTypeInput = findViewById(R.id.crop_type_input)
        nextButton = findViewById(R.id.next_button)
        backButton = findViewById(R.id.back_button)

        // 初始化 Realtime Database
        database = FirebaseDatabase.getInstance().reference.child("sensors")

        // 返回按鈕
        backButton.setOnClickListener {
            finish()
        }

        // 下一步按鈕
        nextButton.setOnClickListener {
            val sensorName = sensorNameInput.text.toString().trim()
            val cropType = cropTypeInput.text.toString().trim()

            if (sensorName.isEmpty() || cropType.isEmpty()) {
                Toast.makeText(this, "請填寫完整資訊", Toast.LENGTH_SHORT).show()
            } else {
                // 建立感測器資料
                val sensorData = mapOf(
                    "sensorName" to sensorName,
                    "cropType" to cropType
                )

                // 將資料儲存到 Realtime Database
                database.push().setValue(sensorData)
                    .addOnSuccessListener {
                        Toast.makeText(this, "資料已儲存，跳轉下一頁", Toast.LENGTH_SHORT).show()
                        val intent = Intent(this, BindingInstructionsActivity::class.java)
                        startActivity(intent)
                    }
                    .addOnFailureListener { exception ->
                        Toast.makeText(this, "新增失敗: ${exception.message}", Toast.LENGTH_SHORT).show()
                    }
            }
        }
    }
}
