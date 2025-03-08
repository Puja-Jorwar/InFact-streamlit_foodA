import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import os
import seaborn as sns
import json
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import base64
from datetime import datetime
import uuid
import requests
from typing import Dict, List





# Page configuration
st.set_page_config(page_title="Food Product Analysis", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
     /* Set the background color for the entire app */
     .stApp {

        background: linear-gradient(to right, #FFD9B3, #FFE5CC, #FFFFFF, #D4F5C1);

       background: linear-gradient(to right, #FF6B6B, #FFA07A, #FFF5E1, #9ACD32);




     }
     
     /* Main container */
     .main {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 10px;
     }
    
     .sidebar-text {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #4CAF50 !important;
        margin-bottom: 20px !important;
     }
    
     .sidebar .stRadio > label {
        font-size: 16px !important;
        color: #2C3E50 !important;
        padding: 8px 0 !important;
     }
    
     .sidebar .stSelectbox > label {
        font-size: 16px !important;
        color: #2C3E50 !important;
        font-weight: 500 !important;
     }
    
     .sidebar .stMultiSelect > label {
        font-size: 16px !important;
        color: #2C3E50 !important;
        font-weight: 500 !important;
     }
    
     .sidebar [data-testid="stMarkdownContainer"] > div {
        padding: 10px 0 !important;
     }
    
     .sidebar [data-testid="stVerticalBlock"] > div {
        padding: 10px 0 !important;
     }
    
     @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
     .title-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
        border-radius: 20px;
        color: brown;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.18),
            inset 0 0 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(8px);
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
     }
    
     .title-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        
        background: linear-gradient(
            45deg,
            rgba(255, 105, 180, 0.1),
            rgba(255, 223, 0, 0.1),
            rgba(0, 255, 255, 0.1)
        );
        z-index: 0;
        animation: shimmer 8s linear infinite;
     }
    
     .animated-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        text-align: center;
        font-size: 3.8rem;
        position: relative;
        background: linear-gradient(
            45deg,
            #FF1493,  /* Deep Pink */
            #FF4500,  /* Orange Red */
            #FFD700,  /* Gold */
            #00FA9A,  /* Medium Spring Green */
            #00BFFF   /* Deep Sky Blue */
        );
        background-size: 300% 300%;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent; /* Keeps the gradient visible */
        padding: 1.5rem;
        margin-bottom: 0.5rem;
        animation: gradient 8s ease infinite, bounce 2s ease-in-out infinite;
        text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2); /* Adds more emphasis */
     }

     .subtitle {
        font-family: 'Poppins', sans-serif;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-size: 1.4rem;
        font-weight: 600;
        margin-top: -0.5rem;
        padding-bottom: 0.5rem;
        animation: fadeIn 1s ease-in;
        position: relative;
     }
    
     .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        animation: fadeInLeft 1s ease-out;
        position: relative;
     }
    
     .logo-container img {
        transition: transform 0.3s ease, filter 0.3s ease;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.2));
     }
    
     .logo-container img:hover {
        transform: scale(1.08) rotate(2deg);
        filter: drop-shadow(0 0 15px rgba(0,0,0,0.3));
     }
    
     @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
     }
    
     @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
     }
    
     @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
     }
    
     @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
     }
    
     @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
     }
    
     /* Responsive design */
     @media (max-width: 768px) {
        .animated-title {
            font-size: 2.5rem;
            padding: 1rem;
        }
        .subtitle {
            font-size: 1.1rem;
        }
     }
    
     /* Food images gallery */
     .image-gallery {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 2rem 0;
     }
    
     .image-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        width: 200px;
     }
    
     /* Footer */
     .footer {
        background: linear-gradient(135deg, #D4F5C1, #FFE5CC); /* Updated gradient */
        color: #2C3E50; /* Dark text color */
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-top: 3rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
     }
    
     .footer-content {
        position: relative;
        z-index: 1;
     }
    
     .footer h2 {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 2rem;
        color: #2C3E50; /* Dark text color */
     }
    
     .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2.5rem;
        margin: 2rem 0;
     }
    
     .footer-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        transition: transform 0.3s ease;
     }
    
     .footer-section:hover {
        transform: translateY(-5px);
     }
    
     .footer-section h3 {
        color: #2C3E50; /* Dark text color */
        margin-bottom: 1.2rem;
        font-size: 1.4rem;
        border-bottom: 2px solid rgba(255, 215, 0, 0.3);
        padding-bottom: 0.5rem;
     }
    
     .footer-section ul {
        list-style: none;
        padding: 0;
     }
    
     .footer-section li {
        margin: 0.8rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
     }
    
     .footer-section li::before {
        content: '✓';
        color: #4CAF50;
        font-weight: bold;
     }
    
     .social-links {
        text-align: center;
        margin-top: 2rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
     }
    
     .social-links a {
        display: inline-block;
        color: #2C3E50; /* Dark text color */
        margin: 0 1rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-decoration: none;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.1);
     }
    
     .social-links a:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
     }
    
     .disclaimer {
        margin-top: 2rem;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
     }
    
     .copyright {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.6);
     }
    
     @media (max-width: 768px) {
        .footer {
            padding: 2rem 1rem;
        }
        .footer-grid {
            gap: 1.5rem;
        }
        .footer h2 {
            font-size: 2rem;
        }
     }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('yes no data.csv')
        data.columns = [col.strip().lower().replace(' ', '_') for col in data.columns]
        data.fillna("N/A", inplace=True)
        return data
    except FileNotFoundError:
        st.error("Dataset file not found!")
        return None

data = load_data()
if data is None:
    st.stop()

# Title section with enhanced layout
col1, col2 = st.columns([1, 5])

with col1:
    if os.path.exists('logo.ico'):
        st.image('logo.ico', width=200)

with col2:
    st.markdown("""
        <div class="title-container">
            <h1 class="animated-title">What's in your Packaged Food?</h1>
            <p class="subtitle">Discover the truth about your food ingredients</p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown('<p class="sidebar-text">🔍 Search & Filter</p>', unsafe_allow_html=True)
    search_query = st.text_input("Search Products", value="", placeholder="Type product name...")
    st.markdown('<hr style="margin: 20px 0;">', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-text">📁 Category</p>', unsafe_allow_html=True)
    category_filter = st.selectbox(
        "",
        options=["All"] + sorted(data["category"].dropna().unique().tolist())
    )
    
    st.markdown('<p class="sidebar-text">🏢 Brand</p>', unsafe_allow_html=True)
    brand_filter = st.multiselect(
        "",
        options=sorted(data["brand"].dropna().unique().tolist())
    )
    
    st.markdown('<p class="sidebar-text">⚠️ Product Safety</p>', unsafe_allow_html=True)
    harmful_filter = st.radio(
        "",
        ["All", "Safe", "Potentially Harmful"]
    )

def display_random_images(num_images=3):
    """
    Display random product images from the available image files in the directory.
    
    Args:
        num_images (int): Number of images to display
    """
    # List all image files
    image_files = [f for f in os.listdir() if f.lower().startswith('img') and 
                   f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        st.warning("No product images found in directory.")
        return
    
    # Select random images
    selected_images = random.sample(image_files, min(num_images, len(image_files)))
    
    # Display images in columns
    cols = st.columns(num_images)
    
    for idx, col in enumerate(cols):
        with col:
            if idx < len(selected_images):
                try:
                    st.image(selected_images[idx],  use_container_width=True)
                except Exception as e:
                    st.error(f"Error loading image: {selected_images[idx]}")
            else:
                st.image("https://placehold.co/200x150/png?text=Food",  use_container_width=True)

display_random_images()

# Filter data
filtered_data = data.copy()
if category_filter != "All":
    filtered_data >>= filtered_data[filtered_data["category"] == category_filter]
if brand_filter:
    filtered_data = filtered_data[filtered_data["brand"].isin(brand_filter)]
if harmful_filter != "All":
    filtered_data = filtered_data[filtered_data["is_harmful?"].str.lower() == harmful_filter.lower()]

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<p style='color: black;'>Total Products</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: black;'>{len(filtered_data)}</h3>", unsafe_allow_html=True)
with col2:
    st.markdown("<p style='color: black;'>Categories</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: black;'>{len(filtered_data['category'].unique())}</h3>", unsafe_allow_html=True)
with col3:
    st.markdown("<p style='color: black;'>Brands</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: black;'>{len(filtered_data['brand'].unique())}</h3>", unsafe_allow_html=True)

# Product list
st.markdown("<h3 style='color: black;'>📊 Product List</h3>", unsafe_allow_html=True)
st.dataframe(
    filtered_data[['product_name', 'brand', 'category', 'is_harmful?']],
    use_container_width=True
)

# Search functionality
vectorizer = TfidfVectorizer()
vectorizer.fit(data['product_name'].dropna())

def search_product(query, data):
    query_vector = vectorizer.transform([query])
    data_vectors = vectorizer.transform(data['product_name'].dropna())
    similarities = cosine_similarity(query_vector, data_vectors).flatten()
    best_match_idx = np.argmax(similarities)
    return data.iloc[best_match_idx], similarities[best_match_idx]

# Search results
if search_query:
    try:
        result, similarity = search_product(search_query, filtered_data)
        if similarity > 0.5:
            st.markdown(f"<h2 style='color: black;'>Details for {result['product_name']}</h2>", unsafe_allow_html=True)
            st.write(result)



            

            # Ingredient composition chart
            harmful = pd.to_numeric(result.get('harmful_ingredient_count', 0), errors='coerce')
            total = pd.to_numeric(result.get('total_ingredients', 0), errors='coerce')
            
            if pd.notnull(total) and pd.notnull(harmful) and total > 0:
                harmful = int(harmful)
                total = int(total)
                non_harmful = total - harmful
                fig, ax = plt.subplots()
                ax.pie(
                    [harmful, non_harmful],
                    labels=['Harmful', 'Non-Harmful'],
                    autopct='%1.1f%%',
                    colors=['#E74C3C', '#2ECC71'],
                    startangle=90
                )
                ax.set_title("Ingredient Composition")
                st.pyplot(fig)
            else:
                st.warning("Ingredient composition data is not available for this product.")

            # Nutritional information
            st.markdown("<h2 style='color: black;'>Nutritional Impact and Alternatives</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: black;'>Nutritional Impact: {result.get('nutritional_impact', 'N/A')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: black;'>Healthy Alternative: {result.get('healthy_alternatives', 'N/A')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: black;'>Alternative Description: {result.get('alternative_description', 'N/A')}</p>", unsafe_allow_html=True)

        else:
            st.warning("No close matches found. Try a different search term.")
    except Exception as e:
        st.error(f"An error occurred: {e}")




def calculate_nutrients(age, gender, weight, height, activity_level):
    """Calculate daily nutrient needs based on user input."""
    # BMR calculation using Harris-Benedict equation
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    # Activity level multipliers
    activity_multipliers = {
        "Sedentary": 1.2,
        "Light Exercise": 1.375,
        "Moderate Exercise": 1.55,
        "Heavy Exercise": 1.725,
        "Athlete": 1.9
    }
    
    daily_calories = bmr * activity_multipliers[activity_level]
    
    # Calculate macronutrients
    nutrients = {
        "Calories": round(daily_calories),
        "Protein (g)": round((daily_calories * 0.3) / 4),  # 30% of calories from protein
        "Carbohydrates (g)": round((daily_calories * 0.4) / 4),  # 40% of calories from carbs
        "Fats (g)": round((daily_calories * 0.3) / 9),  # 30% of calories from fats
    }
    
    return nutrients

def get_food_recommendations(nutrients):
    """Get food recommendations based on calculated nutrients."""
    recommendations = {
        "High Protein Foods": [
            {"food": "Chicken Breast", "serving": "100g", "protein": "31g"},
            {"food": "Greek Yogurt", "serving": "200g", "protein": "20g"},
            {"food": "Eggs", "serving": "2 large", "protein": "12g"},
            {"food": "Lentils", "serving": "200g", "protein": "18g"},
            {"food": "Fish (Salmon)", "serving": "100g", "protein": "25g"}
        ],
        "Complex Carbohydrates": [
            {"food": "Brown Rice", "serving": "100g", "carbs": "23g"},
            {"food": "Sweet Potatoes", "serving": "200g", "carbs": "41g"},
            {"food": "Quinoa", "serving": "100g", "carbs": "21g"},
            {"food": "Oatmeal", "serving": "100g", "carbs": "27g"},
            {"food": "Whole Grain Bread", "serving": "2 slices", "carbs": "24g"}
        ],
        "Healthy Fats": [
            {"food": "Avocado", "serving": "1 medium", "fats": "21g"},
            {"food": "Almonds", "serving": "30g", "fats": "14g"},
            {"food": "Olive Oil", "serving": "1 tbsp", "fats": "14g"},
            {"food": "Chia Seeds", "serving": "30g", "fats": "9g"},
            {"food": "Fatty Fish", "serving": "100g", "fats": "13g"}
        ]
    }
    return recommendations


def add_nutrient_analyzer():
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h2 style='color: #2c3e50; text-align: center;'>🥗 Personalized Nutrition Analysis</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Personal Information")
        age = st.number_input("Age", min_value=15, max_value=100, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        activity_level = st.selectbox("Activity Level", 
            ["Sedentary", "Light Exercise", "Moderate Exercise", "Heavy Exercise", "Athlete"],
            help="Sedentary: Little exercise\nLight: 1-3 days/week\nModerate: 3-5 days/week\nHeavy: 6-7 days/week\nAthlete: 2x/day")
        
        if st.button("Calculate My Needs", use_container_width=True):
            nutrients = calculate_nutrients(age, gender, weight, height, activity_level)
            st.session_state.nutrients = nutrients
            st.session_state.show_recommendations = True

    with col2:
        if 'show_recommendations' in st.session_state and st.session_state.show_recommendations:
            nutrients = st.session_state.nutrients
            
            # Display nutrient needs
            st.markdown("### Your Daily Nutrient Needs")
            fig, ax = plt.subplots(figsize=(8, 4))
            nutrients_display = {k: v for k, v in nutrients.items() if k != "Calories"}
            plt.bar(nutrients_display.keys(), nutrients_display.values(), color=['#FF9999', '#66B2FF', '#99FF99'])
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
            st.markdown(f"**Total Calories Needed:** {nutrients['Calories']} kcal/day")
            
            # Display food recommendations
            st.markdown("### Recommended Foods")
            recommendations = get_food_recommendations(nutrients)
            
            tabs = st.tabs(["Proteins", "Carbs", "Fats"])
            
            with tabs[0]:
                st.markdown("#### High Protein Foods")
                for food in recommendations["High Protein Foods"]:
                    st.markdown(f"• {food['food']} ({food['serving']}) - {food['protein']} protein")
            
            with tabs[1]:
                st.markdown("#### Complex Carbohydrates")
                for food in recommendations["Complex Carbohydrates"]:
                    st.markdown(f"• {food['food']} ({food['serving']}) - {food['carbs']} carbs")
            
            with tabs[2]:
                st.markdown("#### Healthy Fats")
                for food in recommendations["Healthy Fats"]:
                    st.markdown(f"• {food['food']} ({food['serving']}) - {food['fats']} fats")
            
            # Nutrition Tips
            st.markdown("### 💡 Daily Nutrition Tips")
            st.info("""
            • Spread your meals across 4-6 smaller portions throughout the day
            • Drink at least 8 glasses of water daily
            • Include a variety of colorful fruits and vegetables
            • Choose whole grains over refined grains
            • Include lean proteins in every meal
            """)


add_nutrient_analyzer()




# Shopping List Generator
def add_shopping_list_feature():
    st.markdown("## 🛒 Smart Shopping List Generator")
    
    shopping_list = st.session_state.get('shopping_list', [])
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        item = st.text_input("Add item to shopping list")
        if st.button("Add Item"):
            if item:
                shopping_list.append({"item": item, "checked": False})
                st.session_state.shopping_list = shopping_list
    
    with col2:
        if st.button("Clear List"):
            st.session_state.shopping_list = []
            shopping_list = []
    
    for idx, item in enumerate(shopping_list):
        col1, col2 = st.columns([4, 1])
        with col1:
            shopping_list[idx]["checked"] = st.checkbox(
                item["item"],
                value=item["checked"],
                key=f"item_{idx}"
            )
        with col2:
            if st.button("Remove", key=f"remove_{idx}"):
                shopping_list.pop(idx)
                st.session_state.shopping_list = shopping_list
                st.rerun()

# Recipe Suggestion System
def add_recipe_suggestions():
    st.markdown("## 👩‍🍳 Recipe Suggestions")
    
    # Sample recipe database (in practice, this would come from your database)
    recipes = {
        "Healthy Smoothie Bowl": {
            "ingredients": ["banana", "berries", "yogurt", "honey", "granola"],
            "instructions": "Blend fruits, top with granola",
            "difficulty": "Easy",
            "time": "10 mins"
        },
        "Quinoa Salad": {
            "ingredients": ["quinoa", "cucumber", "tomatoes", "feta", "olive oil"],
            "instructions": "Cook quinoa, mix with vegetables",
            "difficulty": "Medium",
            "time": "20 mins"
        }
    }
    
    selected_recipe = st.selectbox("Select a Recipe", list(recipes.keys()))
    
    if selected_recipe:
        recipe = recipes[selected_recipe]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Ingredients")
            for ingredient in recipe["ingredients"]:
                st.markdown(f"- {ingredient}")
        
        with col2:
            st.markdown("### Details")
            st.markdown(f"**Difficulty:** {recipe['difficulty']}")
            st.markdown(f"**Time:** {recipe['time']}")
            st.markdown(f"**Instructions:** {recipe['instructions']}")

# Product Comparison Tool
def add_product_comparison():
    st.markdown("## 🔍 Product Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product1 = st.selectbox("Select First Product", data["product_name"].unique(), key="p1")
    
    with col2:
        product2 = st.selectbox("Select Second Product", data["product_name"].unique(), key="p2")
    
    if product1 and product2:
        comparison_data = {
            "Properties": ["Brand", "Category", "Harmful Ingredients", "Nutritional Impact"],
            "Product 1": [
                data[data["product_name"] == product1]["brand"].iloc[0],
                data[data["product_name"] == product1]["category"].iloc[0],
                data[data["product_name"] == product1]["harmful_ingredient_count"].iloc[0],
                data[data["product_name"] == product1]["nutritional_impact"].iloc[0]
            ],
            "Product 2": [
                data[data["product_name"] == product2]["brand"].iloc[0],
                data[data["product_name"] == product2]["category"].iloc[0],
                data[data["product_name"] == product2]["harmful_ingredient_count"].iloc[0],
                data[data["product_name"] == product2]["nutritional_impact"].iloc[0]
            ]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.table(df_comparison.style.highlight_max(axis=1, color='lightgreen'))

# Ingredient Scanner
def add_ingredient_scanner():
    st.markdown("## 📱 Ingredient Scanner")
    
    # Generate QR code for mobile scanning
    url = "https://your-webapp-url.com/scan"  
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Scan Product")
        st.markdown(f'<img src="data:image/png;base64,{img_str}" alt="QR Code"/>', unsafe_allow_html=True)
        st.markdown("Scan QR code to open mobile scanner")
    
    with col2:
        st.markdown("### Manual Input")
        ingredient_text = st.text_area("Or paste ingredients list here")
        if st.button("Analyze Ingredients"):
            if ingredient_text:
                # Add your ingredient analysis logic here
                st.success("Analysis complete! No harmful ingredients detected.")

# Community Reviews
def add_community_reviews():
    st.markdown("## 💬 Community Reviews")
    
    selected_product = st.selectbox("Select Product to Review", data["product_name"].unique())
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        review_text = st.text_area("Write your review")
        rating = st.slider("Rating", 1, 5, 3)
    
    with col2:
        if st.button("Submit Review"):
            if review_text and rating:
                st.success("Review submitted successfully!")
                
    # Display sample reviews
    st.markdown("### Recent Reviews")
    sample_reviews = [
        {"user": "HealthyEater123", "rating": 4, "text": "Great healthy alternative!"},
        {"user": "NutritionPro", "rating": 5, "text": "Love the ingredients list."}
    ]
    
    for review in sample_reviews:
        st.markdown(f"""
        ⭐ {'★' * review['rating']} {'☆' * (5-review['rating'])}  
        **{review['user']}**: {review['text']}
        """)

# Weekly Meal Planner
def add_meal_planner():
    st.markdown("## 📅 Weekly Meal Planner")
    
    # Get current week dates
    today = datetime.now()
    week_dates = [(today + timedelta(days=i)).strftime("%A, %B %d") for i in range(7)]
    
    meal_types = ["Breakfast", "Lunch", "Dinner"]
    
    # Create weekly plan
    st.markdown("### Plan Your Week")
    
    for date in week_dates:
        st.markdown(f"#### {date}")
        cols = st.columns(len(meal_types))
        
        for idx, meal in enumerate(meal_types):
            with cols[idx]:
                st.markdown(f"**{meal}**")
                meal_input = st.text_input(
                    "",
                    key=f"{date}_{meal}",
                    placeholder=f"Enter {meal.lower()} plan..."
                )


def main():
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Shopping List", 
        "Recipe Suggestions",
        "Product Comparison",
        "Ingredient Scanner",
        "Community Reviews",
        "Meal Planner"
    ])
    
    with tab1:
        add_shopping_list_feature()
    
    with tab2:
        add_recipe_suggestions()
    
    with tab3:
        add_product_comparison()
    
    with tab4:
        add_ingredient_scanner()
    
    with tab5:
        add_community_reviews()
    
    with tab6:
        add_meal_planner()

if __name__ == "__main__":
    main()
    



class ShoppingCart:
    def __init__(self):
        self.items: Dict[str, int] = {}  # product_id: quantity
        self.cart_id = str(uuid.uuid4())
        
    def add_item(self, product_id: str, quantity: int = 1):
        if product_id in self.items:
            self.items[product_id] += quantity
        else:
            self.items[product_id] = quantity
            
    def remove_item(self, product_id: str):
        if product_id in self.items:
            del self.items[product_id]
            
    def update_quantity(self, product_id: str, quantity: int):
        if quantity > 0:
            self.items[product_id] = quantity
        else:
            self.remove_item(product_id)
            
    def get_total_items(self) -> int:
        return sum(self.items.values())
    
    def clear(self):
        self.items.clear()

class Order:
    def __init__(self, cart: ShoppingCart, user_details: Dict):
        self.order_id = str(uuid.uuid4())
        self.cart = cart
        self.user_details = user_details
        self.created_at = datetime.now()
        self.status = "pending"
        
    def to_dict(self) -> Dict:
        return {
            "order_id": self.order_id,
            "items": self.cart.items,
            "user_details": self.user_details,
            "created_at": self.created_at.isoformat(),
            "status": self.status
        }

def initialize_session_state():
    if 'cart' not in st.session_state:
        st.session_state.cart = ShoppingCart()
    if 'orders' not in st.session_state:
        st.session_state.orders = []
    if 'product_database' not in st.session_state:
        # Initialize with sample product database
        st.session_state.product_database = {
            "p1": {
                "name": "Organic Quinoa",
                "price": 12.99,
                "stock": 50,
                "seller": "HealthyFoods Direct",
                "rating": 4.5,
                "description": "100% organic quinoa, rich in protein and fiber",
                "image_url": "quinoa.jpg",
                "purchase_links": {
                    "Amazon": "https://amazon.com/...",
                    "Walmart": "https://walmart.com/...",
                    "Direct": "https://your-store.com/..."
                }
            },
            # Add more products as needed
        }

def add_ecommerce_features():
    st.markdown("## 🛒 Shop Products")
    
    # Initialize session state
    initialize_session_state()
    
    # Create tabs for different shopping features
    shop_tab, cart_tab, orders_tab = st.tabs(["Shop", "Cart", "Orders"])
    
    with shop_tab:
        display_product_listings()
    
    with cart_tab:
        display_shopping_cart()
    
    with orders_tab:
        display_orders()

def display_product_listings():
    st.markdown("### Available Products")
    
    # Filter and sort options
    col1, col2, col3 = st.columns(3)
    with col1:
        sort_by = st.selectbox(
            "Sort by",
            ["Price: Low to High", "Price: High to Low", "Rating", "Popularity"]
        )
    with col2:
        price_range = st.slider(
            "Price Range",
            0.0, 100.0, (0.0, 100.0),
            step=5.0
        )
    with col3:
        category = st.multiselect(
            "Category",
            ["Organic", "Gluten-Free", "Vegan", "Non-GMO"]
        )
    
    # Display products in a grid
    products_per_row = 3
    product_list = list(st.session_state.product_database.items())
    
    for i in range(0, len(product_list), products_per_row):
        cols = st.columns(products_per_row)
        for j in range(products_per_row):
            if i + j < len(product_list):
                product_id, product = product_list[i + j]
                with cols[j]:
                    display_product_card(product_id, product)

def display_product_card(product_id: str, product: Dict):
    """Display individual product card with purchase options"""
    st.markdown(f"""
        <div style="
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
        ">
            <h4>{product['name']}</h4>
            <p>Price: ${product['price']:.2f}</p>
            <p>Rating: {'⭐' * int(product['rating'])}</p>
            <p>{product['description']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Purchase options
    st.markdown("#### Buy from:")
    for platform, link in product['purchase_links'].items():
        if st.button(f"Buy on {platform}", key=f"{product_id}_{platform}"):
            st.markdown(f"<a href='{link}' target='_blank'>Click here to purchase</a>", unsafe_allow_html=True)
    
    # Add to cart
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=product['stock'],
        value=1,
        key=f"qty_{product_id}"
    )
    
    if st.button("Add to Cart", key=f"add_{product_id}"):
        st.session_state.cart.add_item(product_id, quantity)
        st.success(f"Added {quantity} {product['name']} to cart!")

def display_shopping_cart():
    st.markdown("### Your Shopping Cart")
    
    cart = st.session_state.cart
    if not cart.items:
        st.info("Your cart is empty")
        return
    
    total_price = 0
    
    for product_id, quantity in cart.items.items():
        product = st.session_state.product_database[product_id]
        price = product['price'] * quantity
        total_price += price
        
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f"**{product['name']}**")
        with col2:
            st.markdown(f"${product['price']:.2f} x {quantity}")
        with col3:
            st.markdown(f"${price:.2f}")
        with col4:
            if st.button("Remove", key=f"remove_{product_id}"):
                cart.remove_item(product_id)
                st.rerun()
    
    st.markdown(f"### Total: ${total_price:.2f}")
    
    # Checkout section
    st.markdown("### Checkout")
    with st.form("checkout_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
        
        with col2:
            address = st.text_area("Shipping Address")
            payment_method = st.selectbox(
                "Payment Method",
                ["Credit Card", "PayPal", "Apple Pay"]
            )
        
        if st.form_submit_button("Place Order"):
            if name and email and phone and address:
                user_details = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "address": address,
                    "payment_method": payment_method
                }
                
                # Create order
                order = Order(cart, user_details)
                st.session_state.orders.append(order)
                
                # Clear cart
                cart.clear()
                
                st.success(f"Order placed successfully! Order ID: {order.order_id}")
                st.balloons()
            else:
                st.error("Please fill in all required fields")

def display_orders():
    st.markdown("### Your Orders")
    
    if not st.session_state.orders:
        st.info("No orders yet")
        return
    
    for order in st.session_state.orders:
        with st.expander(f"Order {order.order_id} - {order.created_at.strftime('%Y-%m-%d %H:%M')}"):
            st.markdown(f"**Status:** {order.status}")
            st.markdown("#### Items:")
            for product_id, quantity in order.cart.items.items():
                product = st.session_state.product_database[product_id]
                st.markdown(f"- {product['name']} x {quantity}")
            
            st.markdown("#### Shipping Details:")
            for key, value in order.user_details.items():
                st.markdown(f"**{key.title()}:** {value}")

def add_price_comparison():
    st.markdown("## 💰 Price Comparison")
    
    selected_product = st.selectbox(
        "Select Product",
        [p["name"] for p in st.session_state.product_database.values()]
    )
    
    if selected_product:
        # Get product details
        product = next(p for p in st.session_state.product_database.values() if p["name"] == selected_product)
        
        st.markdown("### Available Sellers")
        
        # Create comparison table
        comparison_data = []
        for platform, link in product["purchase_links"].items():
            # In a real application, you would fetch real-time prices
            comparison_data.append({
                "Platform": platform,
                "Price": f"${product['price']:.2f}",
                "Shipping": "Free" if platform == "Direct" else "$5.99",
                "Delivery Time": "2-3 days",
                "Buy": link
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        st.table(df_comparison)
        
        # Price history chart (sample data)
        st.markdown("### Price History")
        price_history = {
            "Date": pd.date_range(end=datetime.now(), periods=30, freq='D'),
            "Price": [product['price'] + np.random.uniform(-2, 2) for _ in range(30)]
        }
        df_history = pd.DataFrame(price_history)
        st.line_chart(df_history.set_index("Date"))


def main():
    
    
    # Add new e-commerce features
    add_ecommerce_features()
    
    # Add price comparison feature
    add_price_comparison()

if __name__ == "__main__":
    main()

def add_nutritional_tracker():
    st.markdown("## 🍎 Nutritional Tracker")
    
    # Initialize session state for nutritional tracking
    if 'nutrition_log' not in st.session_state:
        st.session_state.nutrition_log = []
    
    # Input form for adding food items
    with st.form("nutrition_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            food_item = st.text_input("Food Item")
        with col2:
            calories = st.number_input("Calories", min_value=0)
        with col3:
            protein = st.number_input("Protein (g)", min_value=0)
        
        if st.form_submit_button("Add Food"):
            if food_item and calories and protein:
                st.session_state.nutrition_log.append({
                    "food_item": food_item,
                    "calories": calories,
                    "protein": protein
                })
                st.success("Food item added to log!")
    
    # Display nutritional log
    st.markdown("### Daily Nutritional Log")
    if st.session_state.nutrition_log:
        df_nutrition = pd.DataFrame(st.session_state.nutrition_log)
        st.dataframe(df_nutrition)
        
        # Calculate totals
        total_calories = df_nutrition["calories"].sum()
        total_protein = df_nutrition["protein"].sum()
        
        st.markdown(f"**Total Calories:** {total_calories} kcal")
        st.markdown(f"**Total Protein:** {total_protein} g")
    else:
        st.info("No food items logged yet.")


add_nutritional_tracker()

def add_meal_planner_with_grocery_list():
    st.markdown("## 🥗 Meal Planner with Grocery List")
    
    # Initialize session state for meal planner
    if 'meal_plan' not in st.session_state:
        st.session_state.meal_plan = {
            "Monday": {"Breakfast": "", "Lunch": "", "Dinner": ""},
            "Tuesday": {"Breakfast": "", "Lunch": "", "Dinner": ""},
            "Wednesday": {"Breakfast": "", "Lunch": "", "Dinner": ""},
            "Thursday": {"Breakfast": "", "Lunch": "", "Dinner": ""},
            "Friday": {"Breakfast": "", "Lunch": "", "Dinner": ""},
            "Saturday": {"Breakfast": "", "Lunch": "", "Dinner": ""},
            "Sunday": {"Breakfast": "", "Lunch": "", "Dinner": ""},
        }
    
    # Meal planner form
    st.markdown("### Plan Your Meals")
    for day, meals in st.session_state.meal_plan.items():
        st.markdown(f"#### {day}")
        cols = st.columns(3)
        for idx, (meal_type, meal) in enumerate(meals.items()):
            with cols[idx]:
                st.session_state.meal_plan[day][meal_type] = st.text_input(
                    meal_type,
                    value=meal,
                    key=f"{day}_{meal_type}"
                )
    
    # Generate grocery list
    if st.button("Generate Grocery List"):
        grocery_list = set()
        for day, meals in st.session_state.meal_plan.items():
            for meal in meals.values():
                if meal:
                    grocery_list.update(meal.split(", "))
        
        st.markdown("### Grocery List")
        if grocery_list:
            for item in grocery_list:
                st.markdown(f"- {item}")
        else:
            st.info("No items in the grocery list.")

add_meal_planner_with_grocery_list()

def add_health_goal_tracker():
    st.markdown("## 🏋️‍♂️ Health Goal Tracker")
    
    # Initialize session state for health goals
    if 'health_goals' not in st.session_state:
        st.session_state.health_goals = []
    
    # Input form for setting health goals
    with st.form("health_goal_form"):
        goal_type = st.selectbox("Goal Type", ["Weight Loss", "Muscle Gain", "Maintenance"])
        target = st.number_input("Target (kg or % body fat)", min_value=0.0)
        deadline = st.date_input("Deadline")
        
        if st.form_submit_button("Add Goal"):
            st.session_state.health_goals.append({
                "goal_type": goal_type,
                "target": target,
                "deadline": deadline,
                "progress": []
            })
            st.success("Health goal added!")
    
    # Display health goals and progress
    st.markdown("### Your Health Goals")
    if st.session_state.health_goals:
        for idx, goal in enumerate(st.session_state.health_goals):
            with st.expander(f"{goal['goal_type']} - Target: {goal['target']} by {goal['deadline']}"):
                # Progress tracking
                progress_value = st.number_input(
                    "Current Progress",
                    min_value=0.0,
                    key=f"progress_{idx}"
                )
                if st.button("Update Progress", key=f"update_{idx}"):
                    goal["progress"].append({
                        "date": datetime.now().date(),
                        "value": progress_value
                    })
                    st.success("Progress updated!")
                
                # Progress chart
                if goal["progress"]:
                    df_progress = pd.DataFrame(goal["progress"])
                    st.line_chart(df_progress.set_index("date"))
    else:
        st.info("No health goals set yet.")

add_health_goal_tracker()

def add_recipe_nutrition_calculator():
    st.markdown("## 🥘 Recipe Nutrition Calculator")
    
    # Input form for recipe ingredients
    with st.form("recipe_form"):
        recipe_name = st.text_input("Recipe Name")
        ingredients = st.text_area("Ingredients (one per line)")
        
        if st.form_submit_button("Calculate Nutrition"):
            if recipe_name and ingredients:
                # Sample nutrition data (in practice, use a nutrition API)
                nutrition_data = {
                    "Calories": 0,
                    "Protein (g)": 0,
                    "Carbohydrates (g)": 0,
                    "Fats (g)": 0
                }
                
                # Calculate nutrition (sample logic)
                for ingredient in ingredients.split("\n"):
                    if "chicken" in ingredient.lower():
                        nutrition_data["Calories"] += 100
                        nutrition_data["Protein (g)"] += 20
                    elif "rice" in ingredient.lower():
                        nutrition_data["Calories"] += 200
                        nutrition_data["Carbohydrates (g)"] += 45
                    # Add more ingredients as needed
                
                st.markdown(f"### Nutrition for {recipe_name}")
                st.write(nutrition_data)
            else:
                st.error("Please enter a recipe name and ingredients.")
add_recipe_nutrition_calculator()

def add_food_expiry_tracker():
    st.markdown("## 📅 Food Expiry Tracker")
    
    # Initialize session state for food items
    if 'food_items' not in st.session_state:
        st.session_state.food_items = []
    
    # Input form for adding food items
    with st.form("food_item_form"):
        food_name = st.text_input("Food Item")
        expiry_date = st.date_input("Expiry Date")
        
        if st.form_submit_button("Add Food Item"):
            if food_name and expiry_date:
                st.session_state.food_items.append({
                    "food_name": food_name,
                    "expiry_date": expiry_date
                })
                st.success("Food item added!")
    
    # Display food items and expiry dates
    st.markdown("### Your Food Items")
    if st.session_state.food_items:
        for idx, item in enumerate(st.session_state.food_items):
            days_until_expiry = (item["expiry_date"] - datetime.now().date()).days
            st.markdown(f"**{item['food_name']}** - Expires on {item['expiry_date']} ({days_until_expiry} days left)")
            
            if days_until_expiry <= 0:
                st.error("This item has expired!")
            elif days_until_expiry <= 3:
                st.warning("This item is about to expire!")
    else:
        st.info("No food items added yet.")

add_food_expiry_tracker()



def calculate_recipe_calories(ingredients: List[str]):
    """
    Calculate total calories for a recipe.
    """
    calorie_data = {
        "chicken": 165,  # per 100g
        "rice": 130,     # per 100g
        "olive oil": 884, # per 100ml
        "potato": 77,    # per 100g
        "tomato": 18,    # per 100g
        # Add more ingredients as needed
    }
    
    total_calories = 0
    for ingredient in ingredients:
        for key, value in calorie_data.items():
            if key in ingredient.lower():
                total_calories += value
    return total_calories

def add_recipe_calorie_calculator():
    st.markdown("## 🧮 Recipe Calorie Calculator")
    
    ingredients = st.text_area("Enter recipe ingredients (one per line)", placeholder="e.g., 100g chicken, 200g rice...")
    
    if st.button("Calculate Calories"):
        if ingredients:
            total_calories = calculate_recipe_calories(ingredients.split("\n"))
            st.success(f"Total Calories: {total_calories} kcal")
        else:
            st.error("Please enter recipe ingredients.")


def main():
    
    add_recipe_calorie_calculator()

if __name__ == "__main__":
    main()

   

def add_food_pyramid():
    st.markdown("## 🏔️ Interactive Food Pyramid")
    
    # Food pyramid data
    food_pyramid = {
        "Grains": ["Bread", "Rice", "Pasta"],
        "Vegetables": ["Carrots", "Broccoli", "Spinach"],
        "Fruits": ["Apples", "Bananas", "Oranges"],
        "Protein": ["Chicken", "Fish", "Beans"],
        "Dairy": ["Milk", "Cheese", "Yogurt"],
        "Fats/Oils": ["Olive Oil", "Butter", "Nuts"]
    }
    
    # Display pyramid
    for category, foods in food_pyramid.items():
        with st.expander(f"🍎 {category}"):
            st.markdown(f"**Examples:** {', '.join(foods)}")
            st.markdown(f"**Recommended Servings:** 3-5 per day")

def main():
    
    add_food_pyramid()

if __name__ == "__main__":
    main()



# Enhanced Footer
st.markdown("""
    <div class="footer" style="background: linear-gradient(135deg, #A3B7E0, #F2A3A3, #FCE6A4);">
        <h2 style="color: black;">About In-Fact</h2>
        <div class="footer-grid">
            <div class="footer-section">
                <h3 style="color: black;">Our Mission</h3>
                <p style="color: black;">In-Fact empowers consumers with detailed insights about their food products, 
                helping them make informed decisions about their nutrition and health.</p>
            </div>
            <div class="footer-section">
                <h3 style="color: black;">Key Features</h3>
                <ul>
                    <li style="color:black;">✓ Real-time ingredient analysis</li>
                    <li style="color: black;">✓ Health impact assessment</li>
                    <li style="color: black;">✓ Alternative product suggestions</li>
                    <li style="color: black;">✓ Brand comparison tools</li>
                </ul>
            </div>
            <div class="footer-section">
                <h3 style="color: black;">Contact Us</h3>
                <p style="color: black;">📧 Email: infactsap2025@gmail.com</p>
                <p style="color: black;">📱 Phone: +91 XXXXXXXXXX</p>
                <p style="color: black;">📍 PDEA COEM, Pune</p>
            </div>
        </div>
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: black;">Follow us on social media:</p>
            <div style="margin: 1rem 0;">
                <a href="#" style="color: black; margin: 0 1rem;">Facebook</a>
                <a href="#" style="color: black; margin: 0 1rem;">Twitter</a>
                <a href="#" style="color: black; margin: 0 1rem;">Instagram</a>
            </div>
            <p style="color: black; margin-top: 1rem;">
                &copy; 2025 Team In-Fact Pune. All rights reserved.
            </p>
        </div>
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: black;">Disclaimer: The information provided in this application is for educational purposes only and should not be considered as medical advice. Always consult with a healthcare professional for dietary recommendations.</p>
        </div>
    </div>
""", unsafe_allow_html=True)


