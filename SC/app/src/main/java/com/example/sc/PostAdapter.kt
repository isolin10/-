import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.sc.Post
import com.example.sc.R

class PostAdapter(private val postList: List<Post>) : RecyclerView.Adapter<PostAdapter.PostViewHolder>() {

    class PostViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val usernameTextView: TextView = itemView.findViewById(R.id.username)
        val profileImageView: ImageView = itemView.findViewById(R.id.profile_image)
        val postImageView: ImageView = itemView.findViewById(R.id.post_image)
        val contentTextView: TextView = itemView.findViewById(R.id.content)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PostViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_post, parent, false)
        return PostViewHolder(view)
    }

    override fun onBindViewHolder(holder: PostViewHolder, position: Int) {
        val post = postList[position]

        holder.usernameTextView.text = post.username
        holder.contentTextView.text = post.content

        // 使用 Glide 加載使用者頭像和貼文圖片
        Glide.with(holder.itemView.context)
            .load(post.profileImageUrl)
            .placeholder(R.drawable.ic_profile)
            .into(holder.profileImageView)

        Glide.with(holder.itemView.context)
            .load(post.imageUrl)
            .into(holder.postImageView)
    }

    override fun getItemCount() = postList.size
}
