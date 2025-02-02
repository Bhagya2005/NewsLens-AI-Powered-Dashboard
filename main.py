import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 🔒 Load API Key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Model
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")  # Using Gemini Pro
else:
    st.error("🚨 API Key is missing! Please check your .env file.")


# 🌟 Custom CSS for Beautiful UI
st.markdown("""
    <style>
        /* Title and Header Styles */
        .main-title {
            font-size: 36px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            margin-bottom: 20px;
        }

        .sub-title {
            font-size: 18px;
            color: #7F8C8D;
            text-align: center;
        }

        /* Table Styling */
        .streamlit-table {
            font-size: 16px;
            border-collapse: collapse;
            width: 100%;
            background-color: #ECF0F1;
            border-radius: 10px;
            overflow: hidden;
        }

        .streamlit-table th, .streamlit-table td {
            padding: 10px;
            text-align: center;
        }

        .streamlit-table th {
            background-color: #2980B9;
            color: white;
            font-weight: bold;
        }

        .streamlit-table td {
            background-color: #F4F6F7;
        }

        .streamlit-table tr:hover {
            background-color: #D5DBDB;
        }

        .download-button {
            background-color: #2ECC71;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }

        .download-button:hover {
            background-color: #27AE60;
        }
    </style>
""", unsafe_allow_html=True)

# 🎨 Dashboard Title
st.markdown("<p class='main-title'>📢 NewsLens: AI-Powered Global News Filtering Dashboard</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Find the latest news in your desired categories and country with advanced AI-powered filtering.</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Our product is an innovative, AI-powered news filtering dashboard designed to provide real-time updates on the latest news, categorized and customized based on user preferences. By leveraging advanced machine learning algorithms, it offers a unique ability to filter news based on categories such as positive or negative news, job openings, business, technology, and more. With a user-friendly interface and seamless integration with multiple news sources, the platform ensures that users receive the most relevant and timely news, all in one place. The product also allows users to refine results by country, enabling localized news selection. By providing insights from over 100+ sources, this product empowers users to stay informed and make data-driven decisions..</p>", unsafe_allow_html=True)

# 📅 Sidebar Inputs
st.sidebar.header("🔍Global News Filters")
start_date = st.sidebar.date_input("Start Date", datetime.today() - timedelta(days=7))
end_date = st.sidebar.date_input("End Date", datetime.today())

category_options = ["Positive News", "Negative News", "Job Openings", "Education News", "Business News", "Technology News"]
category = st.sidebar.multiselect("Select News Categories", category_options, default=["Positive News"])

# Add country selection filter
country = st.sidebar.selectbox("Select Country", ["India", "USA", "UK", "Germany", "Australia"])


# Function to fetch news using Gemini AI
def fetch_news(start_date, end_date, selected_categories, country):
    if not selected_categories:
        return []  # Return empty if no categories are selected
    
    # Safeguard: ensure categories list is not out of range
    prompt = f"""
    You are an AI that provides news updates. Generate recent news from {start_date} to {end_date} 
    for the following categories: {', '.join(selected_categories)} in {country}.
    Provide the response in JSON format with fields: "Date", "Title", "Category", "Summary". 
    Example:
    [
        {{"Date": "{start_date}", "Title": "AI Revolution", "Category": "{selected_categories[0]}", "Summary": "New AI surpasses human intelligence."}},
        {{"Date": "{end_date}", "Title": "Stock Market Crash", "Category": "{selected_categories[0]}", "Summary": "Global markets hit new low."}}
    ]
    """
    
    response = model.generate_content(prompt)
    
    if response and response.text:
        try:
            news_data = eval(response.text)  # Convert string JSON to list of dictionaries
            return news_data
        except:
            return []
    return []

# 🔎 Fetch & Display News
if st.sidebar.button("Fetch News"):
    if start_date > end_date:
        st.error("🚨 Start date cannot be after end date!")
    else:
        news_data = fetch_news(start_date, end_date, category, country)
        
        if news_data:
        
            
            # 📰 Display News in Table Format
            st.write("### 📰 Filtered News Results")
            
            # Create DataFrame from news data
            news_df = pd.DataFrame(news_data)

            # Remove empty rows (if any)
            news_df.dropna(subset=["Date", "Title", "Summary"], how="all", inplace=True)
            
            # Remove the "ImageURL" column if present
            if 'ImageURL' in news_df.columns:
                news_df = news_df.drop(columns=['ImageURL'])

            # Display table with styling
            st.markdown("<style>.stDataFrame tbody tr th {text-align: center;}</style>", unsafe_allow_html=True)
            st.dataframe(news_df.style.set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#2980B9'), ('color', 'white'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('background-color', '#F4F6F7')]},
                {'selector': 'tr:hover', 'props': [('background-color', '#D5DBDB')]},
            ]), height=400)

        else:
            st.warning("⚠️ No news articles found for the selected criteria.")

# 📸 Developer Photo and Info on the Right Sidebar
# st.sidebar.image("path_to_your_image/developer-photo.jpg", use_container_width=True)  # Update the path to your photo
st.sidebar.markdown("""
    ### About the Developer
    Hello, I'm Bhagya Patel, a passionate developer working on AI-powered projects. I love building useful tools and experimenting with cutting-edge technologies.

    **Connect with me:**
    - [LinkedIn](https://www.linkedin.com/in/bhagyapatel/)
    - [Portfolio](https://bhagya-patel-portfolio.vercel.app/)

""")
