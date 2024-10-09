package com.example.sc

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.storage.FirebaseStorage
import java.util.UUID

class ProfileFragment : Fragment() {

    private lateinit var auth: FirebaseAuth
    private lateinit var database: DatabaseReference
    private lateinit var profileImageView: ImageView
    private val PICK_IMAGE_REQUEST = 1
    private val storage = FirebaseStorage.getInstance()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_profile, container, false)

        val usernameTextView = view.findViewById<TextView>(R.id.user_id)
        val logoutButton = view.findViewById<Button>(R.id.logout_button)
        profileImageView = view.findViewById(R.id.profile_image)

        // Initialize Firebase Auth and Database
        auth = FirebaseAuth.getInstance()
        database = FirebaseDatabase.getInstance().reference

        val user = auth.currentUser
        if (user != null) {
            val userId = user.uid

            // Fetch username and profile image from Firebase Realtime Database
            database.child("Users").child(userId).get().addOnSuccessListener { snapshot ->
                val username = snapshot.child("username").value.toString()
                val profileImageUrl = snapshot.child("profileImageUrl").value?.toString()

                usernameTextView.text = username

                // 如果有 profileImageUrl，則載入圖片
                profileImageUrl?.let { url ->
                    Glide.with(this)
                        .load(url)
                        .placeholder(R.drawable.ic_profile) // 加載中的佔位符
                        .into(profileImageView)
                }

            }.addOnFailureListener {
                Toast.makeText(context, "無法獲取使用者資料", Toast.LENGTH_SHORT).show()
            }
        }

        profileImageView.setOnClickListener {
            // Open gallery to select image
            val intent = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
            startActivityForResult(intent, PICK_IMAGE_REQUEST)
        }

        logoutButton.setOnClickListener {
            auth.signOut()
            val intent = Intent(activity, LoginActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
        }

        return view
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == PICK_IMAGE_REQUEST && resultCode == Activity.RESULT_OK && data != null) {
            val imageUri: Uri? = data.data
            imageUri?.let {
                uploadProfileImage(it)
            }
        }
    }

    private fun uploadProfileImage(imageUri: Uri) {
        val user = auth.currentUser ?: return
        val userId = user.uid
        val fileName = UUID.randomUUID().toString()
        val storageRef = storage.reference.child("profileImages/$userId/$fileName")

        storageRef.putFile(imageUri)
            .addOnSuccessListener {
                storageRef.downloadUrl.addOnSuccessListener { downloadUri ->
                    // Save download URL to Realtime Database
                    database.child("Users").child(userId).child("profileImageUrl").setValue(downloadUri.toString())
                        .addOnSuccessListener {
                            Toast.makeText(context, "頭像已更新", Toast.LENGTH_SHORT).show()
                            // 更新頭像顯示
                            Glide.with(this)
                                .load(downloadUri)
                                .placeholder(R.drawable.ic_profile) // 替換成你的預設圖片
                                .into(profileImageView)
                        }
                        .addOnFailureListener {
                            Toast.makeText(context, "更新頭像失敗", Toast.LENGTH_SHORT).show()
                        }
                }
            }
            .addOnFailureListener {
                Toast.makeText(context, "上傳頭像失敗", Toast.LENGTH_SHORT).show()
            }
    }
}
