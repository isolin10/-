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
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.ValueEventListener
import com.google.firebase.storage.FirebaseStorage
import java.util.UUID

class PostFragment : Fragment() {

    private lateinit var saveDraftButton: Button
    private lateinit var publishButton: Button
    private lateinit var uploadDataSwitch: Switch
    private lateinit var sensorSpinner: Spinner
    private lateinit var flexboxLayout: FlexboxLayout
    private lateinit var uploadImageButton: Button
    private lateinit var postContent: EditText
    private lateinit var subjectInput: EditText
    private lateinit var addSubject: TextView
    private lateinit var addLocation: TextView
    private lateinit var saveToAlbum: TextView

    private val PICK_IMAGE_REQUEST = 1
    private var selectedImageUris = mutableListOf<Uri>()
    private val db = FirebaseDatabase.getInstance().reference
    private val storage = FirebaseStorage.getInstance()
    private val auth = FirebaseAuth.getInstance()

    // 感測器相關變數
    private val sensorList = mutableListOf<String>()
    private val sensorMap = mutableMapOf<String, String>() // 儲存感測器名稱和其 ID

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_post, container, false)

        // Initialize UI components
        saveDraftButton = view.findViewById(R.id.save_draft_button)
        publishButton = view.findViewById(R.id.publish_button)
        uploadDataSwitch = view.findViewById(R.id.upload_data_switch)
        sensorSpinner = view.findViewById(R.id.sensor_spinner)
        flexboxLayout = view.findViewById(R.id.flexbox_layout)
        uploadImageButton = createUploadButton()
        postContent = view.findViewById(R.id.post_content)
        addSubject = view.findViewById(R.id.add_subject)
        subjectInput = view.findViewById(R.id.subject_input)
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

        addSubject.setOnClickListener {
            toggleSubjectInput()
        }

        // 載入感測器資料
        loadSensorData()

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
                selectedImageUris.add(it)
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
            selectedImageUris.remove(imageUri)
            Toast.makeText(requireContext(), "圖片已刪除", Toast.LENGTH_SHORT).show()
        }

        // Add image view before the upload button
        flexboxLayout.addView(imageView, flexboxLayout.childCount - 1)
    }

    private fun publishPost() {
        val content = postContent.text.toString().trim()
        val subject = subjectInput.text.toString().trim() // 取得主題名稱
        val user = auth.currentUser

        if (user == null || selectedImageUris.isEmpty() || content.isEmpty() || subject.isEmpty()) {
            Toast.makeText(requireContext(), "請填寫所有必填內容", Toast.LENGTH_SHORT).show()
            return
        }

        val userId = user.uid

        // Fetch user data from Realtime Database
        db.child("Users").child(userId).get().addOnSuccessListener { snapshot ->
            val username = snapshot.child("username").value?.toString() ?: "Unknown"
            val profileImageUrl = snapshot.child("profileImageUrl").value?.toString() ?: ""

            val uploadImageUrls = mutableListOf<String>()

            selectedImageUris.forEachIndexed { index, uri ->
                val fileName = UUID.randomUUID().toString()
                val storageRef = storage.reference.child("posts/$fileName")

                storageRef.putFile(uri)
                    .addOnSuccessListener {
                        storageRef.downloadUrl.addOnSuccessListener { downloadUri ->
                            uploadImageUrls.add(downloadUri.toString())
                            if (uploadImageUrls.size == selectedImageUris.size) {
                                savePostToRealtimeDatabase(content, subject, uploadImageUrls, username, profileImageUrl, userId)
                            }
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

    private fun savePostToRealtimeDatabase(content: String, subject: String, imageUrls: List<String>, username: String, profileImageUrl: String, userId: String) {
        val postId = db.child("posts").push().key ?: return

        val post = Post(
            postId = postId,
            userId = userId,
            username = username,
            profileImageUrl = profileImageUrl,
            content = content,
            subject = subject, // 新增主題
            imageUrls = imageUrls,
            timestamp = System.currentTimeMillis(),
            likes = 0
        )

        db.child("posts").child(postId)
            .setValue(post)
            .addOnSuccessListener {
                Toast.makeText(requireContext(), "貼文已發布", Toast.LENGTH_SHORT).show()
                postContent.text.clear()
                subjectInput.text.clear()
                selectedImageUris.clear()
                flexboxLayout.removeAllViews()
                flexboxLayout.addView(uploadImageButton)
            }
            .addOnFailureListener {
                Toast.makeText(requireContext(), "貼文發布失敗", Toast.LENGTH_SHORT).show()
            }
    }

    private fun toggleSubjectInput() {
        if (subjectInput.visibility == View.GONE) {
            subjectInput.visibility = View.VISIBLE
        } else {
            subjectInput.visibility = View.GONE
        }
    }

    private fun saveDraft() {
        // Save draft logic here
    }

    private fun loadSensorData() {
        val database = FirebaseDatabase.getInstance().reference.child("sensors")
        database.addListenerForSingleValueEvent(object : ValueEventListener {
            override fun onDataChange(snapshot: DataSnapshot) {
                sensorList.clear()
                sensorMap.clear()

                for (sensorSnapshot in snapshot.children) {
                    val sensorName = sensorSnapshot.child("sensorName").value?.toString() ?: "未知感測器"
                    val sensorId = sensorSnapshot.key ?: continue
                    sensorList.add(sensorName)
                    sensorMap[sensorName] = sensorId
                }

                // 更新 Spinner 的選項
                val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, sensorList)
                adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
                sensorSpinner.adapter = adapter
            }

            override fun onCancelled(error: DatabaseError) {
                Toast.makeText(requireContext(), "感測器資料加載失敗", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
