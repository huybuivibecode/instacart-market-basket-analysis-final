import streamlit as st
from recommender import AssociationRecommender
import os

# Page config
st.set_page_config(page_title="E-Commerce Product Recommender", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .product-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        background-color: #f9f9f9;
        transition: transform 0.2s;
    }
    .product-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .recommendation-card {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
        transition: transform 0.2s;
    }
    .recommendation-card:hover {
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
        transform: translateY(-2px);
    }
    .cart-item {
        background: linear-gradient(135deg, #fff9e6 0%, #fffde7 100%);
        padding: 8px;
        margin: 4px 0;
        border-radius: 5px;
        border-left: 4px solid #FFC107;
    }
    h1, h2, h3 {
        color: #1a1a1a;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🛒 E-Commerce Product Recommendation System")

# Display hero banner
if os.path.exists("images/banner.jpg"):
    st.image("images/banner.jpg", use_column_width=True)

# Spacer
st.markdown("")

# Select cluster
cluster = st.selectbox("Select Customer Segment (Cluster)", [0, 1, 2], help="Choose cluster to customize recommendations")

# Initialize or update recommender based on cluster
if 'recommender' not in st.session_state or st.session_state.get('current_cluster') != cluster:
    try:
        st.session_state.recommender = AssociationRecommender(cluster)
        st.session_state.current_cluster = cluster
        st.session_state.cart = []  # Reset cart when cluster changes
        st.success(f"✅ Loaded rules for cluster {cluster}")
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

recommender = st.session_state.recommender

# Get all available products
all_products = recommender.get_all_products()

# Display summary metrics
col_metric1, col_metric2, col_metric3 = st.columns(3)
with col_metric1:
    st.metric(label="📦 Total Products", value=len(all_products))
with col_metric2:
    st.metric(label="🛒 Items in Cart", value=len(st.session_state.cart))
with col_metric3:
    st.metric(label="⭐ Cluster", value=f"Segment {cluster}")

# Function to get image URL for a product (group by keywords)
def get_product_image(product_name):
    product_lower = product_name.lower()
    
    # Group by keywords and use base images
    if 'yogurt' in product_lower:
        return 'images/yogurt.jpg'
    elif 'milk' in product_lower:
        return 'images/milk.jpg'
    elif 'juice' in product_lower or 'cider' in product_lower:
        return 'images/juice.jpg'
    elif 'water' in product_lower:
        return 'images/water.jpg'
    elif 'bread' in product_lower:
        return 'images/bread.jpg'
    elif 'avocado' in product_lower:
        return 'images/avocado.jpg'
    elif 'banana' in product_lower:
        return 'images/banana.jpg'
    elif 'strawberr' in product_lower:
        return 'images/strawberry.jpg'
    elif 'spinach' in product_lower or 'greens' in product_lower or 'leafy' in product_lower:
        return 'images/spinach.jpg'
    elif 'apple' in product_lower:
        return 'images/apples.jpg'
    elif 'organic' in product_lower:
        return 'images/organic.jpg'
    elif 'beef' in product_lower or 'ground' in product_lower:
        return 'images/beef.jpg'
    elif 'chicken' in product_lower:
        return 'images/chicken.jpg'
    elif 'salad' in product_lower or 'mix' in product_lower:
        return 'images/salad.jpg'
    elif 'cheese' in product_lower:
        return 'images/100_Grated_Parmesan_Cheese.jpg'
    elif 'popcorn' in product_lower:
        return 'images/100_Calorie_Per_Bag_Popcorn.jpg'
    elif 'pumpkin' in product_lower:
        return 'images/100_Pure_Pumpkin.jpg'
    elif 'flour' in product_lower:
        return 'images/All_Purpose_Flour.jpg'
    elif 'pasta' in product_lower:
        return 'images/Angel_Hair_Pasta.jpg'
    elif 'asparagus' in product_lower:
        return 'images/Asparagus.jpg'
    else:
        # Fallback to online placeholder
        return f"https://via.placeholder.com/150x150?text={product_name[:20].replace(' ', '+')}"


def add_product_to_cart(product_name):
    if product_name not in st.session_state.cart:
        st.session_state.cart.append(product_name)
        st.success(f"Added {product_name} to cart!")
    else:
        st.warning("Already in cart!")

# Sidebar for cart
with st.sidebar:
    st.header("🛍️ Shopping Cart")
    if st.session_state.cart:
        st.info(f"✨ You have **{len(st.session_state.cart)}** item(s) in your cart")
        st.divider()
        for idx, item in enumerate(st.session_state.cart, 1):
            st.markdown(f'<div class="cart-item">**{idx}.** {item}</div>', unsafe_allow_html=True)
        st.divider()
        col_clear = st.columns([1, 1])
        with col_clear[0]:
            if st.button("🗑️ Clear Cart", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        with col_clear[1]:
            st.metric("Total", len(st.session_state.cart), label_visibility="collapsed")
    else:
        st.write("🎁 Your cart is empty. Start shopping!")
        st.info("👉 Pick a product below to begin")

# Separator
st.markdown("---")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.cart:
        st.subheader("🏷️ All Available Products")
        st.caption("Browse and add more items to your collection")
        products_to_display = all_products
    else:
        st.subheader("🔥 Popular Products (Trending Now)")
        st.caption("Start with our most popular items based on customer demand")
        products_to_display = recommender.get_top_products_by_support(top_n=20)
    
    # Display products in a grid
    cols = st.columns(3)
    for i, product in enumerate(products_to_display):
        with cols[i % 3]:
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            st.image(get_product_image(product), width=120)
            st.write(f"**{product}**")
            st.button(f"Add {product[:20]}...", key=f"add_{i}", on_click=add_product_to_cart, args=(product,))
            st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.subheader("💡 Smart Recommendations")
    if st.session_state.cart:
        st.caption("Products you might like based on your cart")
        recommendations = recommender.recommend(st.session_state.cart, top_n=10)
        if recommendations:
            st.info("✨ Personalized for you")
            for product, confidence in recommendations:
                st.markdown(f'<div class="recommendation-card">', unsafe_allow_html=True)
                st.image(get_product_image(product), width=100)
                st.write(f"**{product}**")
                st.write(f"Match: {confidence*100:.1f}%")
                st.button(f"Add {product[:15]}...", key=f"rec_{product}", on_click=add_product_to_cart, args=(product,))
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No recommendations available for your cart items.")
    else:
        st.write("🎯 Add products to your cart to get personalized recommendations!")
        st.info("Our smart algorithm will suggest complementary items based on your selections.")

# Footer
st.markdown("---")
st.markdown("""
### 📖 How It Works

**Our Smart Recommendation System:**
1. Choose a customer segment (cluster) that matches your profile
2. Browse featured products or all available items
3. Add products to your cart that interest you
4. Get AI-powered recommendations based on association rules
5. The more you add, the smarter the recommendations become!

**Features:**
- 📊 Association Rules Analysis - Based on real Instacart purchase patterns
- 🎯 Smart Confidence Scoring - Intelligent product matching
- 🔄 Real-time Updates - Recommendations update as you shop
- 📦 Multiple Clusters - Customized for different customer segments

---
*Built with Streamlit | Data-driven e-commerce recommendations*
""")
