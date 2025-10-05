import streamlit as st
import pandas as pd
import os
import generate_fashion_dataset  

dataset_path = "improved_fashion_dataset_detailed.txt"

# Generate dataset if missing
if not os.path.exists(dataset_path):
    print("Dataset not found. Generating now...")
    generate_fashion_dataset.main()
    print("Dataset generated successfully!")

# ========== ✨ Combined & Optimized CSS ==========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

/* ========== Global Styling ========== */
body {
    background: radial-gradient(circle at top, #0a0a0a 0%, #1a1a1a 60%, #000000 100%);
    font-family: 'Poppins', sans-serif;
    color: #f5f5f5;
}
.stApp {
    background: transparent;
    padding: 24px;
}

/* ========== Main Title ========== */
h1 {
    text-align: center;
    background: linear-gradient(90deg, #FFD700, #FFB000);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    letter-spacing: 3px;
    font-size: 42px;
    text-transform: uppercase;
    margin-top: -15px;
    margin-bottom: 30px;
    text-shadow: 0 0 15px rgba(255,215,0,0.3);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0f0f0f;
    border-right: 3px solid #d4af37;
    box-shadow: 0 0 20px rgba(212,175,55,0.15);
    padding: 24px;
}

/* Card Design */
.card {
    background: #1b1b1b;
    border-radius: 16px;
    padding: 18px;
    margin: 10px;
    border: 1px solid rgba(212,175,55,0.2);
    box-shadow: 0 4px 15px rgba(212,175,55,0.15);
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(212,175,55,0.35);
}
.card-title {
    font-size: 20px;
    font-weight: 600;
    color: #FFD700;
    margin-bottom: 8px;
}
.card-text {
    font-size: 14px;
    color: #d1d1d1;
    margin: 6px 0;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #F4C430, #FFB300);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px 26px;
    border: none;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: #d4af37;
    transform: translateY(-3px);
    box-shadow: 0 0 15px rgba(212,175,55,0.5);
}

/* Inputs & Labels */
.stSelectbox label, .stSidebar label {
    color: #f5f5f5;
    font-weight: 600;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# ========== ⚙️ Load Data ==========
@st.cache_data
def load_data():
    file_path = 'improved_fashion_dataset_detailed.txt'
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep='\t')
    else:
        st.error(f"Dataset file '{file_path}' not found in {os.getcwd()}")
        return None

# ========== 🧠 Recommendation Logic ==========
def recommend_items(df, gender, body_type, skin_tone, height, season):
    filtered_df = df.copy()
    
    # Strict gender and season filters
    if gender != "All":
        filtered_df = filtered_df[filtered_df['gender'] == gender]
    if season != "All":
        filtered_df = filtered_df[filtered_df['season'].isin([season, 'All-season'])]

    filtered_df['score'] = 0.0
    
    # Weighted scoring
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

    # Color match
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

    # Final ranking
    filtered_df = filtered_df[filtered_df['score'] >= 0.8].sort_values(by='score', ascending=False).head(12)
    return filtered_df

# ========== 🚀 Main App ==========
def main():
    st.title("Fashionify")
    df = load_data()
    if df is None:
        return

    # Sidebar filters
    st.sidebar.header("Your Style Preferences")
    gender = st.sidebar.selectbox("Gender", ["All", "Men", "Women"])
    body_type = st.sidebar.selectbox("Body Type", ["All"] + sorted(df['suitable_body_type'].str.split('|').explode().unique()))
    skin_tone = st.sidebar.selectbox("Skin Tone", ["All"] + sorted(df['suitable_skin_tone'].str.split('|').explode().unique()))
    height = st.sidebar.selectbox("Height Range", ["All"] + sorted(df['suitable_height_range'].str.split('|').explode().unique()))
    season = st.sidebar.selectbox("Season", ["All"] + sorted(df['season'].unique()))

    # Button
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
