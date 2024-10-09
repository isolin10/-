package com.example.sc

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import androidx.fragment.app.Fragment

class SensorFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_sensor, container, false)

        // Find the button and set click listener
        val addButton: Button = view.findViewById(R.id.add_sensor_button)
        addButton.setOnClickListener {
            // Show a Toast message when the button is clicked
            Toast.makeText(requireContext(), "新增感測器按鈕點擊", Toast.LENGTH_SHORT).show()
        }

        return view
    }
}
