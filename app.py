import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import requests
from bs4 import BeautifulSoup

# Database Connection
conn = sqlite3.connect("mining_data.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS production (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT, ore_extracted REAL, ore_processed REAL, ore_transported REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT, role TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT, description TEXT, assigned_to TEXT, status TEXT)''')
conn.commit()

# Sidebar Navigation
st.sidebar.title("MinAlytics - Mining Information & Analytics")
page = st.sidebar.radio("Go to", ["Upload Data", "Production Dashboard", "Mining Regulations", "Web Scraping Updates", "Task Management", "Oncoming Feature"])

if page == "Upload Data":
    st.title("Upload Mining Data")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])  
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        for _, row in df.iterrows():
            c.execute("INSERT INTO production (date, ore_extracted, ore_processed, ore_transported) VALUES (?, ?, ?, ?)",
                      (row["date"], row["ore_extracted"], row["ore_processed"], row["ore_transported"]))
        conn.commit()
        st.success("Data uploaded successfully!")

elif page == "Production Dashboard":
    st.title("Production Tracking & Analytics")
    df = pd.read_sql("SELECT * FROM production", conn)
    st.dataframe(df)
    fig = px.line(df, x='date', y=['ore_extracted', 'ore_processed', 'ore_transported'], title="Production Trends")
    st.plotly_chart(fig)

elif page == "Mining Regulations":
    st.title("Mining Knowledge Interface")
    query = st.text_input("Ask a question about Zimbabwe mining regulations:")
    if query:
        response = "According to Zimbabwean Mining Act, ... (Example Response)"
        st.write(response)

elif page == "Web Scraping Updates":
    st.title("Regulatory Updates")
    url = "https://www.mines.gov.zw/latest-news"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    updates = soup.find_all("p")
    for update in updates[:5]:
        st.write(update.text)

elif page == "Task Management":
    st.title("Task Management")
    role = st.selectbox("Select Role", ["Admin", "Head of Department", "Mining Engineer"])
    if role == "Admin":
        st.subheader("Manage Users")
        username = st.text_input("Enter username")
        if st.button("Add User"):
            c.execute("INSERT INTO users (username, role) VALUES (?, ?)", (username, "Mining Engineer"))
            conn.commit()
            st.success("User added successfully!")
    elif role == "Head of Department":
        st.subheader("Assign Tasks")
        task_title = st.text_input("Task Title")
        task_desc = st.text_area("Task Description")
        assigned_to = st.text_input("Assign to (Username)")
        if st.button("Create Task"):
            c.execute("INSERT INTO tasks (title, description, assigned_to, status) VALUES (?, ?, ?, ?)", (task_title, task_desc, assigned_to, "In Progress"))
            conn.commit()
            st.success("Task assigned successfully!")
    elif role == "Mining Engineer":
        st.subheader("View Tasks")
        df_tasks = pd.read_sql("SELECT * FROM tasks WHERE assigned_to = ?", conn, params=(st.text_input("Enter your username"),))
        st.dataframe(df_tasks)

elif page == "Oncoming Feature":
    st.title("Future AI & Computer Vision Capabilities")
    st.write("This feature will leverage deep learning for geoscientific data analysis. Stay tuned!")

# Close Database Connection
conn.close()
