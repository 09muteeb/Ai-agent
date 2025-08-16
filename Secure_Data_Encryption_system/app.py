import streamlit as st
import json
import os
import hashlib
from cryptography.fernet import Fernet

# ---------- Helpers ----------
def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return key

def get_fernet():
    return Fernet(load_key())

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_data():
    if os.path.exists("stored_data.json"):
        with open("stored_data.json", "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open("stored_data.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------- Init Session State ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "view" not in st.session_state:
    st.session_state.view = "Login"

# ---------- Pages ----------
def login_page():
    st.title("🔐 Secure Data Encryption System")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_data()
        if username in users and users[username]["password"] == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.view = "Home"
        else:
            st.error("❌ Invalid username or password")

    if st.button("Create New Account"):
        st.session_state.view = "Register"

def register_page():
    st.title("📝 Create Account")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Register"):
        users = load_data()
        if username in users:
            st.error("⚠️ Username already exists")
        else:
            users[username] = {"password": hash_password(password), "data": {}}
            save_data(users)
            st.success("✅ Account created successfully!")
            st.session_state.view = "Login"

    if st.button("Back to Login"):
        st.session_state.view = "Login"

def home_page():
    st.title("🏠 Home")
    st.write(f"Welcome, **{st.session_state.username}**!")

    if st.button("🔒 Store Data"):
        st.session_state.view = "Store Data"

    if st.button("📂 Retrieve Data"):
        st.session_state.view = "Retrieve Data"

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.view = "Login"

def store_data_page():
    st.title("🔒 Store Encrypted Data")

    data_name = st.text_input("Data Label")
    data_value = st.text_area("Enter Data")

    if st.button("Save"):
        if data_name and data_value:
            fernet = get_fernet()
            encrypted = fernet.encrypt(data_value.encode()).decode()

            users = load_data()
            users[st.session_state.username]["data"][data_name] = encrypted
            save_data(users)

            st.success("✅ Data saved securely!")
        else:
            st.error("⚠️ Please enter both label and data")

    if st.button("⬅ Back"):
        st.session_state.view = "Home"

def retrieve_data_page():
    st.title("📂 Retrieve Data")

    users = load_data()
    data_items = users[st.session_state.username]["data"]

    if not data_items:
        st.warning("⚠️ No data stored yet.")
    else:
        choice = st.selectbox("Select Data", list(data_items.keys()))
        if choice:
            fernet = get_fernet()
            decrypted = fernet.decrypt(data_items[choice].encode()).decode()
            st.text_area("Decrypted Data", decrypted, height=150)

    if st.button("⬅ Back"):
        st.session_state.view = "Home"

# ---------- Router ----------
if not st.session_state.logged_in:
    if st.session_state.view == "Login":
        login_page()
    elif st.session_state.view == "Register":
        register_page()
else:
    if st.session_state.view == "Home":
        home_page()
    elif st.session_state.view == "Store Data":
        store_data_page()
    elif st.session_state.view == "Retrieve Data":
        retrieve_data_page()
