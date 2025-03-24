import streamlit as st
import pandas as pd
import os

# File to store the book data
DATA_FILE = "books.csv"

# Load or create a dataframe
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Title", "Author", "Genre", "Year"])

# Save data to CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Streamlit UI
st.title("📚 Personal Library")

# Load data
df = load_data()

# Sidebar to add books
st.sidebar.header("Add a New Book")
title = st.sidebar.text_input("Title")
author = st.sidebar.text_input("Author")
genre = st.sidebar.text_input("Genre")
year = st.sidebar.number_input("Year", min_value=1000, max_value=9999, step=1, format="%d")

if st.sidebar.button("Add Book"):
    if title and author and genre and year:
        new_entry = pd.DataFrame([[title, author, genre, year]], columns=df.columns)
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
        st.sidebar.success("Book added successfully!")
        st.rerun()
    else:
        st.sidebar.error("Please fill in all fields")

# Search and filter
st.subheader("📖 Your Book Collection")
search = st.text_input("Search by Title, Author, or Genre")
filtered_df = df[df.apply(lambda row: search.lower() in row.to_string().lower(), axis=1)] if search else df
st.dataframe(filtered_df)

# Delete books
if st.button("Clear Library"):
    df = pd.DataFrame(columns=["Title", "Author", "Genre", "Year"])
    save_data(df)
    st.success("Library cleared!")
    st.rerun()
    

# Run the app with: streamlit run personal_library.py
