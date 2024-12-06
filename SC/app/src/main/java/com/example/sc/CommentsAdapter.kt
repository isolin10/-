package com.example.sc

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ktx.getValue

// 数据类，用于存储评论内容
data class Comment(val userId: String = "", val content: String = "", val timestamp: Long = 0)

class CommentsAdapter(private var comments: MutableList<Comment>) :
    RecyclerView.Adapter<CommentsAdapter.CommentViewHolder>() {

    // ViewHolder，用于绑定视图
    class CommentViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val userImageView: ImageView = itemView.findViewById(R.id.comment_user_image)
        val userNameTextView: TextView = itemView.findViewById(R.id.comment_user_name)
        val commentContentTextView: TextView = itemView.findViewById(R.id.comment_content)
        val commentTimeTextView: TextView = itemView.findViewById(R.id.comment_time)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CommentViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_comment, parent, false)
        return CommentViewHolder(view)
    }

    override fun onBindViewHolder(holder: CommentViewHolder, position: Int) {
        val comment = comments[position]

        // 设置留言内容和时间
        holder.commentContentTextView.text = comment.content
        holder.commentTimeTextView.text = java.text.DateFormat.getDateTimeInstance().format(comment.timestamp)

        // 从 Firebase 根据 userId 加载用户数据
        val userRef = FirebaseDatabase.getInstance().reference.child("Users").child(comment.userId)
        userRef.get().addOnSuccessListener { snapshot ->
            if (snapshot.exists()) {
                val userName = snapshot.child("username").value?.toString() ?: "Unknown"
                val profileImageUrl = snapshot.child("profileImageUrl").value?.toString() ?: ""

                // 更新用户名和头像
                holder.userNameTextView.text = userName
                if (profileImageUrl.isNotEmpty()) {
                    Glide.with(holder.itemView.context)
                        .load(profileImageUrl)
                        .placeholder(R.drawable.ic_profile) // 占位图
                        .error(R.drawable.ic_profile) // 加载失败显示默认头像
                        .into(holder.userImageView)
                } else {
                    holder.userImageView.setImageResource(R.drawable.ic_profile) // 默认头像
                }
            } else {
                // 如果用户不存在，显示默认值
                holder.userNameTextView.text = "Unknown"
                holder.userImageView.setImageResource(R.drawable.ic_profile)
                println("User data not found for userId: ${comment.userId}")
            }
        }.addOnFailureListener { exception ->
            // 处理数据加载失败的情况
            holder.userNameTextView.text = "Unknown"
            holder.userImageView.setImageResource(R.drawable.ic_profile)
            println("Failed to load user data for userId: ${comment.userId}. Error: ${exception.message}")
        }
    }

    override fun getItemCount() = comments.size

    // 更新评论列表
    fun updateComments(newComments: List<Comment>) {
        comments.clear()
        comments.addAll(newComments)
        notifyDataSetChanged()
    }
}
