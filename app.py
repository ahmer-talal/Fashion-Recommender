import streamlit as st
import pandas as pd
import os

import generate_fashion_dataset  # Make sure this is imported

dataset_path = "improved_fashion_dataset_detailed.txt"

if not os.path.exists(dataset_path):
    print("Dataset not found. Generating now...")
    generate_fashion_dataset.main()  # or whatever function generates your dataset
    print("Dataset generated successfully!")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

body {
    background: linear-gradient(135deg, #2dd4bf, #a78bfa);
    font-family: 'Inter', sans-serif;
    color: #0f766e;
}
.stApp {
    background: transparent;
    padding: 24px;
}
.sidebar .sidebar-content {
    background: #f9fafb;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-left: 4px solid #2dd4bf;
    animation: slideInLeft 0.5s ease-out;
}
@keyframes slideInLeft {
    0% { opacity: 0; transform: translateX(-20px); }
    100% { opacity: 1; transform: translateX(0); }
}
.card {
    background: #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    margin: 8px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    border: 1px solid transparent;
    background-image: linear-gradient(#e5e7eb, #e5e7eb), linear-gradient(to right, #2dd4bf, #f472b6);
    background-origin: border-box;
    background-clip: padding-box, border-box;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: slideInBottom 0.5s ease-out;
}
.card:nth-child(3n+1) { animation-delay: 0.1s; }
.card:nth-child(3n+2) { animation-delay: 0.2s; }
.card:nth-child(3n+3) { animation-delay: 0.3s; }
@keyframes slideInBottom {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}
.card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4);
    animation: pulseGlow 1.5s infinite;
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4); }
    50% { box-shadow: 0 8px 24px rgba(245, 158, 11, 0.6); }
}
.card-title {
    font-size: 20px;
    font-weight: 600;
    color: #0f766e;
    margin-bottom: 12px;
}
.card-text {
    font-size: 14px;
    color: #6b7280;
    margin: 6px 0;
    display: flex;
    align-items: center;
}
.card-text::before {
    content: '•';
    color: #f59e0b;
    font-size: 16px;
    margin-right: 10px;
}
.stButton>button {
    background: #2dd4bf;
    color: white;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    border: none;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    animation: pulseButton 2s infinite;
    display: block;
    margin: 0 auto;
}
@keyframes pulseButton {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
.stButton>button:hover {
    background: #14b8a6;
    transform: translateY(-2px);
}
.stButton>button:active::after {
    content: '';
    position: absolute;
    width: 100px;
    height: 100px;
    background: rgba(255,255,255,0.3);
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    animation: ripple 0.6s ease-out;
}
@keyframes ripple {
    to { transform: translate(-50%, -50%) scale(2); opacity: 0; }
}
h1 {
    color: white;
    font-size: 32px;
    text-align: center;
    margin-bottom: 24px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    animation: typewriter 2s steps(20) 1s 1 normal both;
    overflow: hidden;
    white-space: nowrap;
}
@keyframes typewriter {
    from { width: 0; }
    to { width: 100%; }
}
.stSelectbox label, .stSidebar label {
    color: #0f766e;
    font-weight: 600;
    font-size: 14px;
}
.stSelectbox div {
    border-radius: 8px;
    transition: border-color 0.3s ease;
}
.stSelectbox div:hover {
    border-color: #f59e0b !important;
}
.stWarning {
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    color: #b91c1c;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #f87171;
}
.stInfo {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    color: #065f46;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #34d399;
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
