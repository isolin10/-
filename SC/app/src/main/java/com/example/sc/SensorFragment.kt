package com.example.sc

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.google.firebase.database.*

class SensorFragment : Fragment() {

    private lateinit var sensorListLayout: LinearLayout
    private lateinit var database: DatabaseReference
    private lateinit var sensorListener: ValueEventListener

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_sensor, container, false)
        sensorListLayout = view.findViewById(R.id.sensor_list_layout)
        database = FirebaseDatabase.getInstance().reference.child("sensors")

        // 新增感測器按鈕
        view.findViewById<View>(R.id.add_sensor_button).setOnClickListener {
            startActivity(Intent(requireContext(), AddSensorActivity::class.java))
        }

        return view
    }

    override fun onStart() {
        super.onStart()

        // 添加监听器以获取数据库数据
        sensorListener = object : ValueEventListener {
            override fun onDataChange(snapshot: DataSnapshot) {
                sensorListLayout.removeAllViews() // 清空视图
                for (sensorSnapshot in snapshot.children) {
                    val sensorName = sensorSnapshot.child("sensorName").value?.toString() ?: "未知感測器"
                    val cropType = sensorSnapshot.child("cropType").value?.toString() ?: "未知作物"

                    // 动态加载自定义布局
                    val sensorView = LayoutInflater.from(requireContext())
                        .inflate(R.layout.sensor_item, sensorListLayout, false)
                    sensorView.findViewById<TextView>(R.id.sensor_name).text = "$sensorName"
                    sensorView.findViewById<TextView>(R.id.crop_type).text = "作物種類：$cropType"

                    // 添加上传按钮
                    val uploadButton = Button(requireContext()).apply {
                        text = "上傳數據"
                        setOnClickListener {
                            // 点击后显示 Toast
                            Toast.makeText(
                                requireContext(),
                                "感測器：$sensorName 資料上傳成功",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    }

                    // 将按钮添加到布局
                    (sensorView as LinearLayout).addView(uploadButton)

                    sensorListLayout.addView(sensorView)
                }
            }

            override fun onCancelled(error: DatabaseError) {
                Toast.makeText(requireContext(), "資料加載失敗: ${error.message}", Toast.LENGTH_SHORT).show()
            }
        }

        database.addValueEventListener(sensorListener)
    }

    override fun onStop() {
        super.onStop()
        database.removeEventListener(sensorListener) // 移除监听器以防止内存泄漏
    }
}
