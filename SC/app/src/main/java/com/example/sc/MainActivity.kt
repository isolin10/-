package com.example.sc

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.LinearLayout
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.google.android.material.bottomnavigation.BottomNavigationView

class MainActivity : AppCompatActivity() {

    private lateinit var searchLayout: LinearLayout
    private lateinit var bottomNavigation: BottomNavigationView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        searchLayout = findViewById(R.id.search_layout)
        bottomNavigation = findViewById(R.id.bottom_navigation)

        bottomNavigation.setOnNavigationItemSelectedListener { item ->
            when (item.itemId) {
                R.id.navigation_home -> {
                    loadFragment(HomeFragment())
                    searchLayout.visibility = View.VISIBLE
                    true
                }
                R.id.navigation_sensor -> {
                    loadFragment(SensorFragment())
                    searchLayout.visibility = View.GONE
                    true
                }
                R.id.navigation_post -> {
                    loadFragment(PostFragment())
                    searchLayout.visibility = View.GONE
                    true
                }
                R.id.navigation_notifications -> {
                    loadFragment(NotificationsFragment())
                    searchLayout.visibility = View.GONE
                    true
                }
                R.id.navigation_profile -> {
                    loadFragment(ProfileFragment()) // 加載 ProfileFragment
                    searchLayout.visibility = View.GONE
                    true
                }
                else -> false
            }
        }
        // 預設載入主頁面 Fragment
        if (savedInstanceState == null) {
            bottomNavigation.selectedItemId = R.id.navigation_home
        }
    }

    private fun loadFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commit()
    }
}
