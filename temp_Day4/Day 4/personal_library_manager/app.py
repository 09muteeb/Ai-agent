import streamlit as st
import pandas as pd

st.set_page_config(page_title="📚 Personal Library Manager", page_icon="📖")

st.title("📚 Personal Library Manager")
st.write("Track the books you own, have read, or want to read.")

# Session state to store books
if "library" not in st.session_state:
    st.session_state.library = pd.DataFrame(columns=["Title", "Author", "Status", "Rating"])

# Add new book
with st.form("Add Book"):
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    status = st.selectbox("Status", ["Unread", "Reading", "Read"])
    rating = st.slider("Rating (if read)", 0, 5, 0)
    submitted = st.form_submit_button("Add Book")
    
    if submitted:
        new_entry = pd.DataFrame([[title, author, status, rating]], 
                                  columns=["Title", "Author", "Status", "Rating"])
        st.session_state.library = pd.concat([st.session_state.library, new_entry], ignore_index=True)
        st.success(f"Added '{title}' by {author}")

# Display library
st.subheader("📖 Your Library")
st.dataframe(st.session_state.library)

# Option to export as CSV
if not st.session_state.library.empty:
    csv = st.session_state.library.to_csv(index=False).encode("utf-8")
    st.download_button("Download Library as CSV", csv, "library.csv", "text/csv")
