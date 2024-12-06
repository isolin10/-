import android.content.Context
import android.content.Intent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.PopupMenu
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.RecyclerView
import androidx.viewpager.widget.PagerAdapter
import androidx.viewpager.widget.ViewPager
import com.bumptech.glide.Glide
import com.example.sc.CommentsBottomSheetFragment
import com.example.sc.PlantDataActivity
import com.example.sc.Post
import com.example.sc.R
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener
import com.tbuonomo.viewpagerdotsindicator.DotsIndicator

class PostAdapter(private val postList: MutableList<Post>) : RecyclerView.Adapter<PostAdapter.PostViewHolder>() {

    class PostViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val usernameTextView: TextView = itemView.findViewById(R.id.username)
        val profileImageView: ImageView = itemView.findViewById(R.id.profile_image)
        val viewPager: ViewPager = itemView.findViewById(R.id.post_viewpager)
        val dotsIndicator: DotsIndicator = itemView.findViewById(R.id.dots_indicator)
        val subjectTextView: TextView = itemView.findViewById(R.id.post_subject)
        val postMenu: ImageView = itemView.findViewById(R.id.post_menu)
        val statisticsButton: ImageView = itemView.findViewById(R.id.statistics_button) // 新的按鈕

        // 愛心與留言的按鈕與計數器
        val likeButton: ImageView = itemView.findViewById(R.id.like_button)
        val likeCountTextView: TextView = itemView.findViewById(R.id.like_count)
        val commentButton: ImageView = itemView.findViewById(R.id.comment_button)
        val commentCountTextView: TextView = itemView.findViewById(R.id.comment_count)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PostViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_post, parent, false)
        return PostViewHolder(view)
    }

    override fun onBindViewHolder(holder: PostViewHolder, position: Int) {
        val post = postList[position]

        holder.usernameTextView.text = post.username
        holder.subjectTextView.text = post.subject ?: "無主題"

        // 使用 Glide 加載使用者頭像
        Glide.with(holder.itemView.context)
            .load(post.profileImageUrl)
            .placeholder(R.drawable.ic_profile)
            .into(holder.profileImageView)

        // 加載多張圖片
        val imageUrls = post.imageUrls ?: emptyList()
        val imageAdapter = ImagePagerAdapter(holder.itemView.context, imageUrls) { imageUrl ->
            // 跳轉到留言頁面 (例如 BottomSheetFragment)
            val activity = holder.itemView.context as AppCompatActivity
            val fragment = CommentsBottomSheetFragment.newInstance(post.postId!!)
            fragment.show(activity.supportFragmentManager, "CommentsBottomSheet")
        }

        holder.viewPager.adapter = imageAdapter
        holder.dotsIndicator.setViewPager(holder.viewPager)

        // 點擊數據按鈕跳轉到數據頁面
        holder.statisticsButton.setOnClickListener {
            val intent = Intent(holder.itemView.context, PlantDataActivity::class.java).apply {
                putExtra("subject", post.subject)
                putExtra("imageUrl", post.imageUrls?.getOrNull(0)) // 傳遞第一張圖片 URL 作為示例
            }
            holder.itemView.context.startActivity(intent)
        }

        // 設置愛心數與留言數
        holder.likeCountTextView.text = post.likes.toString()
        //holder.commentCountTextView.text = post.comments.toString()

        // 點擊愛心按鈕
        holder.likeButton.setOnClickListener {
            val isLiked = post.isLikedByUser

            if (isLiked) {
                post.likes -= 1
                holder.likeButton.setImageResource(R.drawable.ic_heart_outline)
            } else {
                post.likes += 1
                holder.likeButton.setImageResource(R.drawable.ic_heart_filled)
            }

            // 更新 Firebase 中的愛心數
            val database = FirebaseDatabase.getInstance().reference
            database.child("posts").child(post.postId!!).child("likes").setValue(post.likes)

            post.isLikedByUser = !isLiked
            holder.likeCountTextView.text = post.likes.toString()
        }

        // 點擊留言按鈕
        holder.commentButton.setOnClickListener {
            val activity = holder.itemView.context as AppCompatActivity
            val fragment = CommentsBottomSheetFragment.newInstance(post.postId!!)
            fragment.show(activity.supportFragmentManager, "CommentsBottomSheet")
        }

        // 更新 Firebase 中的留言數
        updateCommentCount(post.postId!!, holder.commentCountTextView)

        // 選單功能
        holder.postMenu.setOnClickListener {
            val popupMenu = PopupMenu(holder.itemView.context, holder.postMenu)
            popupMenu.inflate(R.menu.post_menu)
            popupMenu.setOnMenuItemClickListener { menuItem ->
                when (menuItem.itemId) {
                    R.id.delete_post -> {
                        deletePost(holder.itemView.context, post, position)
                        true
                    }
                    else -> false
                }
            }
            popupMenu.show()
        }
    }

    private fun updateCommentCount(postId: String, commentCountTextView: TextView) {
        val database = FirebaseDatabase.getInstance().reference
        database.child("posts").child(postId).child("comments")
            .addListenerForSingleValueEvent(object : ValueEventListener {
                override fun onDataChange(snapshot: DataSnapshot) {
                    val commentCount = snapshot.childrenCount.toInt()
                    commentCountTextView.text = commentCount.toString()
                }

                override fun onCancelled(error: DatabaseError) {
                    // 可選: 錯誤處理
                }
            })
    }


    private fun deletePost(context: Context, post: Post, position: Int) {
        val database = FirebaseDatabase.getInstance().reference
        post.postId?.let {
            database.child("posts").child(it).removeValue()
                .addOnSuccessListener {
                    if (position >= 0 && position < postList.size) {
                        postList.removeAt(position)
                        notifyItemRemoved(position)
                        Toast.makeText(context, "貼文已刪除", Toast.LENGTH_SHORT).show()
                    } else {
                        Toast.makeText(context, "貼文已刪除", Toast.LENGTH_SHORT).show()
                    }
                }
                .addOnFailureListener {
                    Toast.makeText(context, "刪除失敗", Toast.LENGTH_SHORT).show()
                }
        }
    }

    override fun getItemCount() = postList.size
}

// 圖片輪播適配器
class ImagePagerAdapter(
    private val context: Context,
    private val imageUrls: List<String>,
    private val onClick: (String) -> Unit
) : PagerAdapter() {

    override fun instantiateItem(container: ViewGroup, position: Int): Any {
        val imageView = ImageView(context)
        Glide.with(context)
            .load(imageUrls[position])
            .into(imageView)

        // 設置點擊事件
        imageView.setOnClickListener {
            onClick(imageUrls[position])
        }

        container.addView(imageView)
        return imageView
    }

    override fun getCount(): Int {
        return imageUrls.size
    }

    override fun isViewFromObject(view: View, obj: Any): Boolean {
        return view == obj
    }

    override fun destroyItem(container: ViewGroup, position: Int, obj: Any) {
        container.removeView(obj as ImageView)
    }
}
