import streamlit as st
import pandas as pd
import os

import generate_fashion_dataset  

dataset_path = "improved_fashion_dataset_detailed.txt"

if not os.path.exists(dataset_path):
    print("Dataset not found. Generating now...")
    generate_fashion_dataset.main()  # or whatever function generates your dataset
    print("Dataset generated successfully!")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

body {
    background: linear-gradient(135deg, #0d0d0d, #1a1a1a);
    font-family: 'Poppins', sans-serif;
    color: #f5f5f5;
}
.stApp {
    background: transparent;
    padding: 24px;
}
.sidebar .sidebar-content {
    background: #141414;
    border-radius: 12px;
    padding: 24px;
    border-left: 3px solid #d4af37;
    box-shadow: 0 4px 12px rgba(212,175,55,0.1);
}
.card {
    background: #1f1f1f;
    border-radius: 14px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 4px 15px rgba(212,175,55,0.15);
    border: 1px solid rgba(212,175,55,0.2);
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 25px rgba(212,175,55,0.35);
}
.card-title {
    font-size: 20px;
    font-weight: 600;
    color: #d4af37;
    margin-bottom: 8px;
}
.card-text {
    font-size: 14px;
    color: #d1d1d1;
    margin: 6px 0;
}
h1 {
    color: #d4af37;
    font-size: 36px;
    text-align: center;
    margin-bottom: 28px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.stButton>button {
    background: linear-gradient(135deg, #000000, #2c2c2c);
    color: #d4af37;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 600;
    border: 1px solid #d4af37;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: #d4af37;
    color: #0d0d0d;
    transform: translateY(-3px);
    box-shadow: 0 0 15px rgba(212,175,55,0.5);
}
.stSelectbox label, .stSidebar label {
    color: #f5f5f5;
    font-weight: 600;
    font-size: 14px;
}
.stSelectbox div:hover {
    border-color: #d4af37 !important;
}
</style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    file_path = 'improved_fashion_dataset_detailed.txt'
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep='\t')
    else:
        st.error(f"Dataset file '{file_path}' not found in {os.getcwd()}")
        return None

# Recommendation algorithm
def recommend_items(df, gender, body_type, skin_tone, height, season):
    filtered_df = df.copy()
    
    # Strict gender filter
    if gender != "All":
        filtered_df = filtered_df[filtered_df['gender'] == gender]
    
    # Strict season filter
    if season != "All":
        filtered_df = filtered_df[filtered_df['season'].isin([season, 'All-season'])]
    
    # Initialize scores
    filtered_df['score'] = 0.0
    
    # Scoring logic
    if gender != "All":
        filtered_df['score'] += (filtered_df['gender'] == gender) * 0.3
    if body_type != "All":
        filtered_df['score'] += filtered_df['suitable_body_type'].str.contains(body_type, na=False) * 0.2
    if skin_tone != "All":
        filtered_df['score'] += filtered_df['suitable_skin_tone'].str.contains(skin_tone, na=False) * 0.2
    if height != "All":
        filtered_df['score'] += filtered_df['suitable_height_range'].str.contains(height, na=False) * 0.1
    if season != "All":
        filtered_df['score'] += (filtered_df['season'] == season) * 0.2
    
    # Color suitability
    color_suitability = {
        'Apple': ['Black', 'Navy', 'Charcoal', 'Burgundy', 'Indigo', 'Olive', 'Maroon'],
        'Pear': ['Black', 'Maroon', 'Olive', 'Indigo', 'Grey', 'Brown'],
        'Rectangle': ['Coral', 'Mint', 'Sky Blue', 'Lavender', 'Peach', 'Pink', 'Mustard'],
        'Hourglass': ['Red', 'Teal', 'Emerald', 'Pink', 'Violet', 'Gold'],
        'Inverted Triangle': ['Navy', 'Green', 'Mustard', 'Rust', 'Khaki'],
        'Fair': ['Red', 'Blue', 'Pink', 'Mint', 'Lavender', 'Sky Blue'],
        'Medium': ['Teal', 'Coral', 'Mustard', 'Olive', 'Peach'],
        'Tan': ['Cream', 'Gold', 'Emerald', 'Rust', 'Khaki'],
        'Olive': ['Burgundy', 'Indigo', 'Silver', 'Violet', 'Brown'],
        'Dark': ['Mustard', 'Olive', 'Cream', 'Gold', 'White', 'Beige']
    }
    if body_type in color_suitability:
        filtered_df['score'] += filtered_df['color'].isin(color_suitability[body_type]) * 0.2
    if skin_tone in color_suitability:
        filtered_df['score'] += filtered_df['color'].isin(color_suitability[skin_tone]) * 0.2
    
    # Filter and sort
    filtered_df = filtered_df[filtered_df['score'] >= 0.8].sort_values(by='score', ascending=False).head(12)
    
    return filtered_df

# Main app
def main():
    st.title("Fashionify")
    
    df = load_data()
    if df is None:
        return
    
    # Sidebar
    st.sidebar.header("Your Style Preferences")
    gender = st.sidebar.selectbox("Gender", ["All", "Men", "Women"])
    body_type = st.sidebar.selectbox("Body Type", ["All"] + sorted(df['suitable_body_type'].str.split('|').explode().unique()))
    skin_tone = st.sidebar.selectbox("Skin Tone", ["All"] + sorted(df['suitable_skin_tone'].str.split('|').explode().unique()))
    height = st.sidebar.selectbox("Height Range", ["All"] + sorted(df['suitable_height_range'].str.split('|').explode().unique()))
    season = st.sidebar.selectbox("Season", ["All"] + sorted(df['season'].unique()))
    
    if st.button("Get Recommendations"):
        filtered_df = recommend_items(df, gender, body_type, skin_tone, height, season)
        
        if filtered_df.empty:
            st.warning("Koi perfect match nahi mila, dost! Filters thoda loose karo.")
            st.info("Try: Set Season to 'All' or check other body types.")
        else:
            st.subheader("Your Top Picks")
            cols = st.columns(3)
            for idx, row in filtered_df.iterrows():
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-title">{row['name']}</div>
                        <div class="card-text">Category: {row['category']}</div>
                        <div class="card-text">Color: {row['color']}</div>
                        <div class="card-text">Price: {row['price_range']}</div>
                        <div class="card-text">Fit: {row['fit']}</div>
                        <div class="card-text">Occasion: {row['occasion']}</div>
                        <div class="card-text">Season: {row['season']}</div>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
