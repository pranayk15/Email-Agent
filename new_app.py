# app.py
import streamlit as st
from new_email_agent_updated import email_graph

st.set_page_config(page_title="AI Email Agent", page_icon="📧", layout="centered")
st.title("📧 AI Email Agent")

# ------------------ SIDEBAR SMTP LOGIN ---------
st.sidebar.header("🔐 SMTP Login (Required)")

smtp_email = st.sidebar.text_input("Your Email Address")
smtp_password = st.sidebar.text_input("Your App Password (NOT your Gmail password)", type="password")
smtp_server = st.sidebar.text_input("SMTP Server", value="smtp.gmail.com")
smtp_port = st.sidebar.text_input("SMTP Port", value="587")

# ----------- APP PASSWORD HELP SECTION ----------
with st.sidebar.expander("❓ What is an App Password? (Important)"):
    st.markdown("""
### 🔐 What is an App Password?

App Password ≠ Gmail Password  
**You should NOT use your normal Gmail password here.**

Google blocks normal Gmail passwords for apps.  
So you must use a special 16-digit App Password.

### 🛠️ How to create an App Password (Gmail)

1. Go to **https://myaccount.google.com/**
2. Click **Security**
3. Enable **2-Step Verification** (required)
4. After enabling, scroll down to **App Passwords**
5. Select:
   - **App:** Mail  
   - **Device:** Your device  
6. Google will generate a **16-digit password** (example: `abcd efgh ijkl mnop`)
7. **Use THIS password** in the field above.


### ⚠️ Important Notes
- Do **NOT** enter your normal Gmail password → it will fail.
- App password is used ONLY for apps (like this one).
- You can delete or reset it anytime.

""")

def smtp_ready():
    return all([smtp_email, smtp_password, smtp_server, smtp_port])


# ------------------ MAIN UI ---------------------
st.write("Type in natural language what email you want to send.")

prompt = st.text_area(
    "Enter your request (e.g., 'Send an email to test@gmail.com saying hi!')",
    height=150
)

if st.button("Send Email"):
    if not smtp_ready():
        st.error("❌ Please enter your SMTP details in the sidebar first.")
    elif not prompt.strip():
        st.error("❌ Please enter an email instruction.")
    else:
        with st.spinner("Processing and sending email..."):
            try:
                result = email_graph.invoke({
                    "prompt": prompt,
                    "smtp_email": smtp_email,
                    "smtp_password": smtp_password,
                    "smtp_server": smtp_server,
                    "smtp_port": smtp_port
                })

                status = result.get("status", "")

                if "successfully" in status.lower():
                    st.success(status)
                else:
                    st.error(status)

            except Exception as e:
                st.error(f"Error: {e}")
