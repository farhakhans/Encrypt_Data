import streamlit as st
import json
import hashlib
import os

# 📁 User storage file
USER_DB = "users.json"

# Streamlit page settings
st.set_page_config(page_title="Secure Login", layout="centered")

# 🌈 Gradient background
page_bg = """
<style>
.stApp {
    background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
    padding: 2rem;
    min-height: 100vh;
    background-attachment: fixed;
    font-family: 'Arial', sans-serif;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 👤 Creator credit at top-left
credit_html = """
<div style="position: absolute; top: 6px; left: 15px; z-index: 9999;">
    <span style="font-size: 18px; font-weight: bold; color: #fff;">Created by Farhana Ahsan</span>
</div>
"""
st.markdown(credit_html, unsafe_allow_html=True)

# 🔐 Load users from file
def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

# 🔑 Password hashing

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 💾 Save new user
def save_user(username, user_id, password):
    hashed_pw = hash_password(password)
    users = load_users()
    users[user_id] = {"username": username, "password": hashed_pw}
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# ✅ Verify login
def verify_login(user_id, password):
    users = load_users()
    if user_id in users:
        return users[user_id]["password"] == hash_password(password)
    return False

# 🔄 Session management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# 🔓 Logged in view
if st.session_state.logged_in:
    user_info = load_users()[st.session_state.user_id]
    st.success(f"Welcome, {user_info['username']} (User ID: {st.session_state.user_id}) 👋")

    if st.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.rerun()

# 🔐 Not logged in view
else:
    st.title("🔐 Secure Login System")

    menu = st.selectbox("Select Option", ["Login", "Register"])

    if menu == "Register":
        st.subheader("📝 Create New Account")
        username = st.text_input("Username")
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            users = load_users()
            if user_id in users:
                st.error("🚫 This User ID is already taken.")
            else:
                save_user(username, user_id, password)
                st.success("✅ User registered successfully!")

    elif menu == "Login":
        st.subheader("🔑 Login to Your Account")
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_login(user_id, password):
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.success("🎉 Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")
