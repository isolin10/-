package com.example.sc

data class Post(
    val username: String? = null,  // 使用者名稱
    val content: String? = null,  // 貼文內容
    val imageUrl: String? = null,  // 貼文圖片URL
    val profileImageUrl: String? = null,  // 使用者頭像URL
    val timestamp: Long? = null  // 貼文時間戳記
)
