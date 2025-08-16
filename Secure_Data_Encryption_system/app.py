import streamlit as st
import os
from cryptography.fernet import Fernet

# ----------------------------
# Encryption utilities
# ----------------------------

def load_key():
    """Load the secret key from file or generate one if not exists"""
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return key

def get_cipher():
    key = load_key()
    return Fernet(key)

def store_data(key, value):
    cipher = get_cipher()
    encrypted_value = cipher.encrypt(value.encode())
    with open("data.txt", "a") as f:
        f.write(f"{key}:{encrypted_value.decode()}\n")

def retrieve_data(key):
    if not os.path.exists("data.txt"):
        return None
    cipher = get_cipher()
    with open("data.txt", "r") as f:
        for line in f:
            stored_key, stored_value = line.strip().split(":")
            if stored_key == key:
                return cipher.decrypt(stored_value.encode()).decode()
    return None

# ----------------------------
# Streamlit App
# ----------------------------

st.title("🔐 Secure Data Encryption System")

menu = ["Store Data", "Retrieve Data"]
choice = st.sidebar.selectbox("Choose Action", menu)

# Store Data Section
if choice == "Store Data":
    st.subheader("Store Secure Data")
    key = st.text_input("Enter a key (identifier)")
    value = st.text_input("Enter a value to encrypt")

    if st.button("Store Data"):
        if key and value:
            store_data(key, value)
            st.session_state["last_stored"] = f"✅ Stored '{key}: {value}' successfully!"
        else:
            st.session_state["last_stored"] = "⚠️ Please provide both key and value."

    if "last_stored" in st.session_state:
        st.success(st.session_state["last_stored"])

# Retrieve Data Section
elif choice == "Retrieve Data":
    st.subheader("Retrieve Secure Data")
    key = st.text_input("Enter the key to retrieve value")

    if st.button("Retrieve Data"):
        if key:
            result = retrieve_data(key)
            if result:
                st.session_state["last_retrieved"] = f"🔎 Value for '{key}': {result}"
            else:
                st.session_state["last_retrieved"] = f"❌ No data found for key: {key}"
        else:
            st.session_state["last_retrieved"] = "⚠️ Please enter a key."

    if "last_retrieved" in st.session_state:
        st.info(st.session_state["last_retrieved"])
