package com.example.sc

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.ImageView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener

class CommentsBottomSheetFragment : BottomSheetDialogFragment() {

    private lateinit var commentsRecyclerView: RecyclerView
    private lateinit var commentInput: EditText
    private lateinit var sendCommentButton: ImageView
    private lateinit var commentsAdapter: CommentsAdapter

    private var postId: String? = null
    private val database = FirebaseDatabase.getInstance().reference
    private val auth = FirebaseAuth.getInstance()

    companion object {
        fun newInstance(postId: String): CommentsBottomSheetFragment {
            val fragment = CommentsBottomSheetFragment()
            val args = Bundle().apply {
                putString("postId", postId)
            }
            fragment.arguments = args
            return fragment
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        postId = arguments?.getString("postId")
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_comments_bottom_sheet, container, false)

        commentsRecyclerView = view.findViewById(R.id.comments_recycler_view)
        commentInput = view.findViewById(R.id.comment_input)
        sendCommentButton = view.findViewById(R.id.send_comment_button)

        commentsAdapter = CommentsAdapter(mutableListOf())
        commentsRecyclerView.layoutManager = LinearLayoutManager(context)
        commentsRecyclerView.adapter = commentsAdapter

        loadComments()

        sendCommentButton.setOnClickListener {
            val comment = commentInput.text.toString().trim()
            if (comment.isNotEmpty()) {
                postCommentToFirebase(comment)
                commentInput.text.clear()
            }
        }

        return view
    }

    private fun loadComments() {
        postId?.let { postId ->
            database.child("posts").child(postId).child("comments")
                .addValueEventListener(object : ValueEventListener {
                    override fun onDataChange(snapshot: DataSnapshot) {
                        val comments = mutableListOf<Comment>()
                        for (commentSnapshot in snapshot.children) {
                            val comment = commentSnapshot.getValue(Comment::class.java)
                            comment?.let { comments.add(it) }
                        }
                        commentsAdapter.updateComments(comments)
                    }

                    override fun onCancelled(error: DatabaseError) {
                        println("Failed to load comments: ${error.message}")
                    }
                })
        }
    }

    private fun postCommentToFirebase(commentContent: String) {
        val currentUser = auth.currentUser
        if (currentUser == null) {
            println("User not authenticated")
            return
        }

        val userId = currentUser.uid

        // Retrieve user information for the comment
        database.child("Users").child(userId).get().addOnSuccessListener { snapshot ->
            val username = snapshot.child("username").value?.toString() ?: "Unknown"
            val profileImageUrl = snapshot.child("profileImageUrl").value?.toString() ?: ""

            // Prepare comment data
            val commentData = mapOf(
                "userId" to userId,
                "content" to commentContent,
                "timestamp" to System.currentTimeMillis()
            )

            postId?.let { postId ->
                database.child("posts").child(postId).child("comments").push()
                    .setValue(commentData)
                    .addOnSuccessListener {
                        println("Comment posted successfully")
                    }
                    .addOnFailureListener { error ->
                        println("Failed to post comment: ${error.message}")
                    }
            }
        }.addOnFailureListener { error ->
            println("Failed to retrieve user data: ${error.message}")
        }
    }
}
