import streamlit as st
import re

# Page config
st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")

st.title("🔒 Password Strength Meter")
st.write("Check how strong your password is.")

# Input
password = st.text_input("Enter your password", type="password")

# Strength check function
def check_strength(pwd):
    score = 0
    if len(pwd) >= 8:
        score += 1
    if re.search(r"[A-Z]", pwd):
        score += 1
    if re.search(r"[a-z]", pwd):
        score += 1
    if re.search(r"\d", pwd):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
        score += 1

    if score <= 2:
        return "Weak 🔴"
    elif score in (3, 4):
        return "Moderate 🟡"
    else:
        return "Strong 🟢"

# Output
if password:
    st.subheader("Strength:")
    st.write(check_strength(password))
