# secure_data_app.py
import streamlit as st
import hashlib
import json
import os
from cryptography.fernet import Fernet

# ---------- Config / file names ----------
FERNET_KEY_FILE = "fernet.key"
DATA_FILE = "stored_data.json"
MASTER_PASSWORD = "admin123"  # Change this in production

# ---------- Utilities ----------
def ensure_fernet_key():
    """Load existing Fernet key, or generate and save a new one."""
    if os.path.exists(FERNET_KEY_FILE):
        with open(FERNET_KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(FERNET_KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_data():
    """Load stored_data from DATA_FILE (JSON)."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    """Save stored_data to DATA_FILE (JSON)."""
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
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "view" not in st.session_state:
    st.session_state.view = "Home"  # Home, Store, Retrieve, Login

FERNET_KEY = ensure_fernet_key()
fernet = Fernet(FERNET_KEY)
stored_data = load_data()  # format: { "label1": {"encrypted_text": "...", "passkey": "hashed"}, ... }

# ---------- UI ----------
st.title("🔒 Secure Data Encryption System")
st.sidebar.title("Navigation")
st.sidebar.write("Use the menu to move between pages.")
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Go to", menu, index=menu.index(st.session_state.view) if st.session_state.view in menu else 0)
st.session_state.view = choice

# Helper: show stored entries (labels only)
def show_entries():
    if not stored_data:
        st.info("No stored entries yet.")
        return
    st.write("Stored entries:")
    for label in stored_data.keys():
        st.write(f"- **{label}**")

# Home
if st.session_state.view == "Home":
    st.subheader("🏠 Welcome")
    st.write(
        """
        This app stores encrypted text in memory (and optionally persists it to a local file).
        Each entry is saved with a hashed passkey. To retrieve an entry, you must provide the correct passkey.
        After 3 failed attempts you will be required to reauthorize (Login page).
        """
    )
    st.markdown("**Quick actions:**")
    if st.button("Store Data"):
        st.session_state.view = "Store Data"
        st.rerun()
    if st.button("Retrieve Data"):
        st.session_state.view = "Retrieve Data"
        st.experimental_rerun()
    st.write("---")
    show_entries()

# Store Data
elif st.session_state.view == "Store Data":
    st.subheader("📂 Store Data Securely")
    label = st.text_input("Entry label (unique identifier):", placeholder="e.g., my_bank_pin or secret_note")
    user_data = st.text_area("Enter Data (plaintext to encrypt):")
    passkey = st.text_input("Enter Passkey (used to unlock this entry):", type="password")

    if st.button("Encrypt & Save"):
        if not (label and user_data and passkey):
            st.error("All fields are required.")
        elif label in stored_data:
            st.warning("An entry with that label already exists. Choose a different label or remove the old one.")
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
        st.session_state.view = "Home"
        st.experimental_rerun()

# Retrieve Data
elif st.session_state.view == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    if st.session_state.failed_attempts >= 3:
        st.warning("🔒 Too many failed attempts — reauthorization required. Please login from the Login page.")
        if st.button("Go to Login"):
            st.session_state.view = "Login"
            st.experimental_rerun()
    else:
        if not stored_data:
            st.info("No entries stored yet. Use 'Store Data' first.")
        else:
            label = st.selectbox("Choose entry to decrypt:", options=list(stored_data.keys()))
            passkey = st.text_input("Enter passkey to decrypt:", type="password")
            if st.button("Decrypt"):
                if not passkey:
                    st.error("Passkey required.")
                else:
                    entry = stored_data.get(label)
                    if not entry:
                        st.error("Selected entry not found (it may have been removed).")
                    else:
                        hashed = hash_passkey(passkey)
                        if hashed == entry["passkey"]:
                            try:
                                plaintext = decrypt_text(fernet, entry["encrypted_text"])
                                st.success(f"✅ Decrypted data for **{label}**:")
                                st.code(plaintext)
                                st.session_state.failed_attempts = 0
                            except Exception:
                                # Unexpected decryption problem
                                st.error("Decryption error — data corrupted or key mismatch.")
                        else:
                            st.session_state.failed_attempts += 1
                            remaining = max(0, 3 - st.session_state.failed_attempts)
                            st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining}")
                            if st.session_state.failed_attempts >= 3:
                                st.warning("🔒 Too many failed attempts. Redirecting to Login page...")
                                st.session_state.view = "Login"
                                st.experimental_rerun()

    st.write("---")
    if st.button("Back to Home"):
        st.session_state.view = "Home"
        st.experimental_rerun()

# Login (reauthorization)
elif st.session_state.view == "Login":
    st.subheader("🔑 Reauthorization Required")
    st.write("Enter the master password to reset failed attempts and continue.")
    login_pass = st.text_input("Master Password:", type="password")
    if st.button("Login"):
        if login_pass == MASTER_PASSWORD:
            st.success("✅ Reauthorized successfully.")
            st.session_state.failed_attempts = 0
            st.session_state.view = "Retrieve Data"
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect master password.")

    st.write("---")
    if st.button("Back to Home"):
        st.session_state.view = "Home"
        st.experimental_rerun()
