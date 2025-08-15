# app.py
import streamlit as st
import hashlib
import json
import os
from cryptography.fernet import Fernet

# ---------- Config ----------
FERNET_KEY_FILE = "fernet.key"
DATA_FILE = "stored_data.json"
MASTER_PASSWORD = "admin123"

# ---------- Session State ----------
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "view" not in st.session_state:
    st.session_state.view = "Home"

# ---------- Utilities ----------
def ensure_fernet_key():
    if os.path.exists(FERNET_KEY_FILE):
        with open(FERNET_KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(FERNET_KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_passkey(passkey: str) -> str:
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_text(fernet: Fernet, plaintext: str) -> str:
    return fernet.encrypt(plaintext.encode()).decode()

def decrypt_text(fernet: Fernet, ciphertext: str) -> str:
    return fernet.decrypt(ciphertext.encode()).decode()

# ---------- Initialization ----------
st.set_page_config(page_title="🔒 Secure Data System", layout="centered")
FERNET_KEY = ensure_fernet_key()
fernet = Fernet(FERNET_KEY)
stored_data = load_data()

# ---------- UI ----------
st.title("🔒 Secure Data Encryption System")
st.sidebar.title("Navigation")
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox(
    "Go to",
    menu,
    index=menu.index(st.session_state.view) if st.session_state.view in menu else 0
)
st.session_state.view = choice

def show_entries():
    if not stored_data:
        st.info("No stored entries yet.")
        return
    st.write("Stored entries:")
    for label in stored_data.keys():
        st.write(f"- **{label}**")

# ---------- Pages ----------
if st.session_state.view == "Home":
    st.subheader("🏠 Welcome")
    st.write(
        "This app stores encrypted text securely. Use a passkey to encrypt and decrypt data."
    )
    if st.button("Store Data"):
        if st.session_state.view != "Store Data":
            st.session_state.view = "Store Data"
            st.experimental_rerun()
    if st.button("Retrieve Data"):
        if st.session_state.view != "Retrieve Data":
            st.session_state.view = "Retrieve Data"
            st.experimental_rerun()
    st.write("---")
    show_entries()

elif st.session_state.view == "Store Data":
    st.subheader("📂 Store Data Securely")
    label = st.text_input("Entry label:", placeholder="e.g., my_bank_pin")
    user_data = st.text_area("Enter Data (plaintext):")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if not (label and user_data and passkey):
            st.error("All fields are required.")
        elif label in stored_data:
            st.warning("Entry already exists.")
        else:
            hashed_pass = hash_passkey(passkey)
            encrypted_text = encrypt_text(fernet, user_data)
            stored_data[label] = {"encrypted_text": encrypted_text, "passkey": hashed_pass}
            save_data(stored_data)
            st.success(f"✅ Entry '{label}' stored securely.")
            st.session_state.failed_attempts = 0

    st.write("---")
    show_entries()
    if st.button("Back to Home"):
        if st.session_state.view != "Home":
            st.session_state.view = "Home"
            st.experimental_rerun()

elif st.session_state.view == "Retrieve Data":
    st.subheader("🔍 Retrieve Data")
    if st.session_state.failed_attempts >= 3:
        st.warning("🔒 Too many failed attempts — reauthorization required.")
        if st.button("Go to Login"):
            if st.session_state.view != "Login":
                st.session_state.view = "Login"
                st.experimental_rerun()
    else:
        if not stored_data:
            st.info("No entries stored yet.")
        else:
            label = st.selectbox("Choose entry:", options=list(stored_data.keys()))
            passkey = st.text_input("Enter passkey:", type="password")
            if st.button("Decrypt"):
                entry = stored_data.get(label)
                if entry and hash_passkey(passkey) == entry["passkey"]:
                    try:
                        plaintext = decrypt_text(fernet, entry["encrypted_text"])
                        st.success(f"✅ Decrypted data for **{label}**:")
                        st.code(plaintext)
                        st.session_state.failed_attempts = 0
                    except:
                        st.error("Decryption error.")
                else:
                    st.session_state.failed_attempts += 1
                    remaining = max(0, 3 - st.session_state.failed_attempts)
                    st.error(f"❌ Incorrect passkey! Attempts left: {remaining}")
                    if st.session_state.failed_attempts >= 3:
                        if st.session_state.view != "Login":
                            st.session_state.view = "Login"
                            st.experimental_rerun()

    if st.button("Back to Home"):
        if st.session_state.view != "Home":
            st.session_state.view = "Home"
            st.experimental_rerun()

elif st.session_state.view == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Master Password:", type="password")
    if st.button("Login"):
        if login_pass == MASTER_PASSWORD:
            st.success("✅ Reauthorized successfully.")
            st.session_state.failed_attempts = 0
            if st.session_state.view != "Retrieve Data":
                st.session_state.view = "Retrieve Data"
                st.experimental_rerun()
        else:
            st.error("❌ Incorrect master password.")

    if st.button("Back to Home"):
        if st.session_state.view != "Home":
            st.session_state.view = "Home"
            st.experimental_rerun()
