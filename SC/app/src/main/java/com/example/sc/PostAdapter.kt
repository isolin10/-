import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.PopupMenu
import android.widget.TextView
import android.widget.Toast
import androidx.recyclerview.widget.RecyclerView
import androidx.viewpager.widget.ViewPager
import com.bumptech.glide.Glide
import com.example.sc.Post
import com.example.sc.R
import com.google.firebase.database.FirebaseDatabase
import com.tbuonomo.viewpagerdotsindicator.DotsIndicator

class PostAdapter(private val postList: MutableList<Post>) : RecyclerView.Adapter<PostAdapter.PostViewHolder>() {

    class PostViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val usernameTextView: TextView = itemView.findViewById(R.id.username)
        val profileImageView: ImageView = itemView.findViewById(R.id.profile_image)
        val viewPager: ViewPager = itemView.findViewById(R.id.post_viewpager)
        val dotsIndicator: DotsIndicator = itemView.findViewById(R.id.dots_indicator)
        val contentTextView: TextView = itemView.findViewById(R.id.content)
        val postMenu: ImageView = itemView.findViewById(R.id.post_menu)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PostViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_post, parent, false)
        return PostViewHolder(view)
    }

    override fun onBindViewHolder(holder: PostViewHolder, position: Int) {
        val post = postList[position]

        holder.usernameTextView.text = post.username
        holder.contentTextView.text = post.content

        // 使用 Glide 加載使用者頭像
        Glide.with(holder.itemView.context)
            .load(post.profileImageUrl)
            .placeholder(R.drawable.ic_profile)
            .into(holder.profileImageView)

        // 加载多张图片
        val imageUrls = post.imageUrls ?: emptyList()  // Assuming post.imageUrls is a List<String> of image URLs
        val imageAdapter = ImagePagerAdapter(holder.itemView.context, imageUrls)
        holder.viewPager.adapter = imageAdapter
        holder.dotsIndicator.setViewPager(holder.viewPager)

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

class ImagePagerAdapter(private val context: Context, private val imageUrls: List<String>) : RecyclerView.Adapter<ImagePagerAdapter.ImageViewHolder>() {

    class ImageViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val imageView: ImageView = itemView.findViewById(R.id.image_view)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ImageViewHolder {
        val view = LayoutInflater.from(context).inflate(R.layout.item_image, parent, false)
        return ImageViewHolder(view)
    }

    override fun onBindViewHolder(holder: ImageViewHolder, position: Int) {
        val imageUrl = imageUrls[position]
        Glide.with(context)
            .load(imageUrl)
            .into(holder.imageView)
    }

    override fun getItemCount() = imageUrls.size
}
