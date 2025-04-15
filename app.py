import streamlit as st
import re
import random


st.set_page_config(page_title="Password Strength Meter", page_icon="🔐")


st.title("🔐 Password Strength Meter")
st.markdown("Check your password strength and get suggestions to make it stronger!")

blacklist = {"password123", "123456", "qwerty", "letmein", "admin", "password", "abc123"}


special_chars = "!@#$%^&*"


def check_password_strength(password):
    score = 0
    feedback = []

    if password.lower() in blacklist:
        return 1, "❌ This password is too common. Please choose something more unique."

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔸 Make it at least 8 characters long.")

    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("🔸 Add both uppercase and lowercase letters.")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("🔸 Add at least one digit (0–9).")

    if any(char in special_chars for char in password):
        score += 1
    else:
        feedback.append(f"🔸 Add at least one special character ({special_chars}).")

    if score <= 2:
        strength = "❌ Weak"
    elif score <= 4:
        strength = "⚠️ Moderate"
    else:
        strength = "✅ Strong"

    return score, strength if score == 5 else "\n".join(feedback)


def generate_strong_password(length=12):
    if length < 8:
        length = 8
    chars = (
        random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") +
        random.choice("abcdefghijklmnopqrstuvwxyz") +
        random.choice("0123456789") +
        random.choice(special_chars)
    )
    remaining = ''.join(random.choices(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" + special_chars,
        k=length - 4
    ))
    password = list(chars + remaining)
    random.shuffle(password)
    return ''.join(password)


password = st.text_input("🔑 Enter your password", type="password")

if password:
    score, result = check_password_strength(password)
    st.markdown(f"**Score:** {score}/5")

    if score == 5:
        st.success("✅ Strength: Strong — Your password is secure!")
    elif score >= 3:
        st.warning("⚠️ Strength: Moderate")
        st.markdown("Suggestions:\n" + result)
    else:
        st.error("❌ Strength: Weak")
        st.markdown("Suggestions:\n" + result)


st.markdown("---")
st.markdown("Need help coming up with a secure password?")
if st.button("🔄 Generate Strong Password"):
    new_password = generate_strong_password()
    st.code(new_password, language="text")
