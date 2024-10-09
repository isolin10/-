package com.example.sc

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase

class RegisterActivity : AppCompatActivity() {
    private lateinit var auth: FirebaseAuth
    private lateinit var database: DatabaseReference

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        auth = FirebaseAuth.getInstance()
        database = FirebaseDatabase.getInstance().reference

        val emailEditText = findViewById<EditText>(R.id.emailEditText)
        val passwordEditText = findViewById<EditText>(R.id.passwordEditText)
        val confirmPasswordEditText = findViewById<EditText>(R.id.confirmPasswordEditText)
        val usernameEditText = findViewById<EditText>(R.id.userIdEditText) // 改為使用者自訂的 Username
        val registerButton = findViewById<Button>(R.id.registerButton)

        registerButton.setOnClickListener {
            val email = emailEditText.text.toString().trim()
            val password = passwordEditText.text.toString().trim()
            val confirmPassword = confirmPasswordEditText.text.toString().trim()
            val username = usernameEditText.text.toString().trim()

            if (password != confirmPassword) {
                Toast.makeText(this, "Password and confirm password do not match.", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // 註冊使用者
            auth.createUserWithEmailAndPassword(email, password)
                .addOnCompleteListener(this) { task ->
                    if (task.isSuccessful) {
                        val user = auth.currentUser
                        user?.let {
                            // 發送驗證郵件
                            it.sendEmailVerification().addOnCompleteListener { emailTask ->
                                if (emailTask.isSuccessful) {
                                    Toast.makeText(this, "驗證信件已寄送到 $email", Toast.LENGTH_SHORT).show()

                                    // 系統生成的使用者ID和自訂的 Username 儲存到資料庫
                                    val userId = it.uid  // Firebase自動生成的使用者ID
                                    val userMap = mapOf(
                                        "userId" to userId,
                                        "username" to username // 儲存自訂的 Username
                                    )
                                    database.child("Users")
                                        .child(userId)
                                        .setValue(userMap)
                                        .addOnCompleteListener { dbTask ->
                                            if (dbTask.isSuccessful) {
                                                // 成功寫入資料庫後跳轉
                                                navigateToHome()
                                            } else {
                                                Toast.makeText(this, "資料庫更新失敗: ${dbTask.exception?.message}", Toast.LENGTH_SHORT).show()
                                            }
                                        }
                                }
                            }
                        }
                    } else {
                        Toast.makeText(this, "註冊失敗: ${task.exception?.message}", Toast.LENGTH_LONG).show()
                    }
                }
        }
    }

    private fun navigateToHome() {
        val intent = Intent(this, LoginActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)
    }
}
