package com.example.sc

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import com.google.android.flexbox.FlexboxLayout
import com.google.android.material.snackbar.Snackbar
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.storage.FirebaseStorage
import java.util.UUID

class PostFragment : Fragment() {

    private lateinit var saveDraftButton: Button
    private lateinit var publishButton: Button
    private lateinit var uploadDataSwitch: Switch
    private lateinit var flexboxLayout: FlexboxLayout
    private lateinit var uploadImageButton: Button
    private lateinit var postContent: EditText
    private lateinit var addSubject: TextView
    private lateinit var addLocation: TextView
    private lateinit var saveToAlbum: TextView

    private val PICK_IMAGE_REQUEST = 1
    private var selectedImageUri: Uri? = null
    private val db = FirebaseDatabase.getInstance().reference
    private val storage = FirebaseStorage.getInstance()
    private val auth = FirebaseAuth.getInstance()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_post, container, false)

        // Initialize UI components
        saveDraftButton = view.findViewById(R.id.save_draft_button)
        publishButton = view.findViewById(R.id.publish_button)
        uploadDataSwitch = view.findViewById(R.id.upload_data_switch)
        flexboxLayout = view.findViewById(R.id.flexbox_layout)
        uploadImageButton = createUploadButton()
        postContent = view.findViewById(R.id.post_content)
        addSubject = view.findViewById(R.id.add_subject)
        addLocation = view.findViewById(R.id.add_location)
        saveToAlbum = view.findViewById(R.id.save_to_album)

        // Add initial upload button
        flexboxLayout.addView(uploadImageButton)

        // Set up button listeners
        saveDraftButton.setOnClickListener {
            saveDraft()
        }

        publishButton.setOnClickListener {
            publishPost()
        }

        // Handle expandable items
        addSubject.setOnClickListener {
            Snackbar.make(view, "新增主題點擊", Snackbar.LENGTH_SHORT).show()
        }

        addLocation.setOnClickListener {
            Snackbar.make(view, "新增地址點擊", Snackbar.LENGTH_SHORT).show()
        }

        saveToAlbum.setOnClickListener {
            Snackbar.make(view, "儲存至相簿點擊", Snackbar.LENGTH_SHORT).show()
        }

        return view
    }

    private fun createUploadButton(): Button {
        val button = Button(requireContext())
        button.text = "點擊新增圖片"
        button.textSize = 12f
        button.layoutParams = ViewGroup.LayoutParams(250, 250)
        button.setOnClickListener {
            // Open gallery to select image
            val intent = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
            startActivityForResult(intent, PICK_IMAGE_REQUEST)
        }
        return button
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == PICK_IMAGE_REQUEST && resultCode == Activity.RESULT_OK && data != null) {
            val imageUri: Uri? = data.data
            imageUri?.let {
                selectedImageUri = it
                addImageView(it)
            }
        }
    }

    private fun addImageView(imageUri: Uri) {
        val imageView = ImageView(requireContext())
        imageView.setImageURI(imageUri)
        imageView.layoutParams = ViewGroup.LayoutParams(250, 250)
        imageView.setPadding(8, 8, 8, 8)
        imageView.scaleType = ImageView.ScaleType.CENTER_CROP

        // Set click listener to remove image on click
        imageView.setOnClickListener {
            flexboxLayout.removeView(it)
            selectedImageUri = null
            Toast.makeText(requireContext(), "圖片已刪除", Toast.LENGTH_SHORT).show()
        }

        // Add image view before the upload button
        flexboxLayout.addView(imageView, flexboxLayout.childCount - 1)
    }

    private fun saveDraft() {
        // Save draft logic, store content locally
    }

    private fun publishPost() {
        val content = postContent.text.toString().trim()
        val user = auth.currentUser

        if (user == null || selectedImageUri == null || content.isEmpty()) {
            Toast.makeText(requireContext(), "請選擇圖片並填寫內容", Toast.LENGTH_SHORT).show()
            return
        }

        val userId = user.uid

        // Fetch user data from Realtime Database
        db.child("Users").child(userId).get().addOnSuccessListener { snapshot ->
            val username = snapshot.child("username").value.toString()
            val profileImageUrl = snapshot.child("profileImageUrl").value.toString()

            // Upload image to Firebase Storage
            val fileName = UUID.randomUUID().toString()
            val storageRef = storage.reference.child("posts/$fileName")

            selectedImageUri?.let { uri ->
                storageRef.putFile(uri)
                    .addOnSuccessListener {
                        // Image uploaded successfully, get the download URL
                        storageRef.downloadUrl.addOnSuccessListener { downloadUri ->
                            // Save post to Realtime Database with user data
                            savePostToRealtimeDatabase(content, downloadUri.toString(), username, profileImageUrl, userId)
                        }
                    }
                    .addOnFailureListener {
                        Toast.makeText(requireContext(), "圖片上傳失敗", Toast.LENGTH_SHORT).show()
                    }
            }
        }.addOnFailureListener {
            Toast.makeText(requireContext(), "無法獲取用戶資料", Toast.LENGTH_SHORT).show()
        }
    }

    private fun savePostToRealtimeDatabase(content: String, imageUrl: String, username: String, profileImageUrl: String, userId: String) {
        // Create post data
        val post = hashMapOf(
            "userId" to userId,
            "username" to username,
            "profileImageUrl" to profileImageUrl,
            "content" to content,
            "imageUrl" to imageUrl,
            "timestamp" to System.currentTimeMillis()  // 可用於排序貼文
        )

        // Save post to Realtime Database
        db.child("posts").push()
            .setValue(post)
            .addOnSuccessListener {
                Toast.makeText(requireContext(), "貼文已發布", Toast.LENGTH_SHORT).show()
                // Clear input and selected image
                postContent.text.clear()
                selectedImageUri = null
                flexboxLayout.removeAllViews()
                flexboxLayout.addView(uploadImageButton)
            }
            .addOnFailureListener {
                Toast.makeText(requireContext(), "貼文發布失敗", Toast.LENGTH_SHORT).show()
            }
    }
}
