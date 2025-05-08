import streamlit as st
import pandas as pd

# Sample Product Data
products = [
    {"id": 1, "name": "Smartphone A", "price": 499, "rating": 4.5, "stock": True, "brand": "Brand X"},
    {"id": 2, "name": "Smartphone B", "price": 450, "rating": 4.2, "stock": False, "brand": "Brand Y"},
    {"id": 3, "name": "Smartphone C", "price": 350, "rating": 4.8, "stock": True, "brand": "Brand Z"},
    {"id": 4, "name": "Smartphone D", "price": 550, "rating": 4.0, "stock": True, "brand": "Brand X"},
    {"id": 5, "name": "Smartphone E", "price": 299, "rating": 4.7, "stock": True, "brand": "Brand Y"},
]

# Convert to DataFrame for easier manipulation
product_df = pd.DataFrame(products)

# Streamlit App
st.title("Product Details Bot")
st.write("Search and explore products effortlessly!")

# Search Bar
search_query = st.text_input("Enter product name or brand:", "")

# Filter Bar
max_price = st.slider("Max Price:", min_value=100, max_value=1000, value=500, step=50)
show_in_stock = st.checkbox("Show only in-stock products", value=True)

# Search Functionality
filtered_products = product_df[
    (product_df["name"].str.contains(search_query, case=False)) &
    (product_df["price"] <= max_price) &
    (product_df["stock"] | ~show_in_stock)
]

st.write("### Search Results")
if not filtered_products.empty:
    for _, product in filtered_products.iterrows():
        st.subheader(f"{product['name']} (${product['price']})")
        st.write(f"**Brand:** {product['brand']}")
        st.write(f"**Rating:** {product['rating']}")
        st.write("**In Stock:** Yes" if product["stock"] else "**In Stock:** No")
        if st.button(f"View Details: {product['name']}"):
            st.session_state["selected_product"] = product.to_dict()
            st.experimental_rerun()
else:
    st.write("No products found. Please adjust your search.")

# Product Details View
if "selected_product" in st.session_state:
    selected_product = st.session_state["selected_product"]
    st.write("---")
    st.header(f"Details: {selected_product['name']}")
    st.write(f"**Price:** ${selected_product['price']}")
    st.write(f"**Brand:** {selected_product['brand']}")
    st.write(f"**Rating:** {selected_product['rating']} ⭐")
    st.write("**In Stock:** Yes" if selected_product["stock"] else "**In Stock:** No")

    # Recommendations
    st.write("### Recommended Products")
    recommendations = product_df[
        (product_df["brand"] == selected_product["brand"]) &
        (product_df["id"] != selected_product["id"])
    ]
    for _, rec_product in recommendations.iterrows():
        st.write(f"- {rec_product['name']} (${rec_product['price']})")

    # Back Button
    if st.button("Back to Search"):
        del st.session_state["selected_product"]
        st.experimental_rerun()
