# 📧 AI Email Agent (LangGraph + Streamlit + Gemini)

A smart AI-powered email agent built using **LangGraph**, **Google Gemini**, and **Streamlit**.  
Users can simply describe the email they want to send in plain English, and the agent will:

✅ Extract recipient  
✅ Extract subject  
✅ Generate the email body  
✅ Send the email using the user's own SMTP (Gmail App Password)  
✅ Provide full SMTP login instructions  
✅ Run completely client-side (no storing credentials)

---

## 🚀 Live Demo (Streamlit Cloud)

👉 **https://my-app-email-ai-agent.streamlit.app**  
_(Replace this with your actual Streamlit deployed link)_

---

## ✨ Features

### 🔹 1. Natural Language Email Creation  
Users type instructions like:  
> “Send an email to test@gmail.com saying the meeting is at 5 PM.”

The app extracts:
- Recipient  
- Subject  
- Message body  

Automatically.

---

### 🔹 2. User-Side SMTP Login  
Each user provides their own:
- Gmail address  
- Gmail App Password (NOT normal password)  
- SMTP server (default: smtp.gmail.com)  
- Port (default: 587)

This makes the app secure:
- No credentials stored  
- No server-side email sending  
- Works for any Gmail user  

---

### 🔹 3. Built with LangGraph  
The system uses a 2-step LangGraph workflow:
1. **parse_prompt** → AI extracts JSON  
2. **send_email** → sends email via SMTP

---

### 🔹 4. Gemini LLM for Extraction  
Built using : ChatGoogleGenerativeAI (gemini-2.5-flash)
Gemini returns JSON describing the email structure.

---

### 🔹 5. Streamlit Frontend  
Modern UI with:
- SMTP sidebar login  
- App Password tutorial + screenshot  
- Text prompt input  
- Send button  
- Real-time status updates  

---

## 📂 Project Structure
```
email-agent/
│── app.py 
│── new_email_agent.py
│── requirements.txt 
│── .gitignore 
│── .env (local only) # Do NOT upload to Github
```

---

## 🧠 Tech Stack

| Component    | Technology       |
| ------------ | ---------------- |
| LLM          | Gemini 2.5 Flash |
| AI Framework | LangGraph        |
| UI           | Streamlit        |
| Email        | SMTP (Gmail)     |
| DevOps       | Streamlit Cloud  |

---

## ⚙️ Installation & Setup (Local)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/pranayk15/email-agent.git
cd email-agent
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Create .env file (local only)
```ini
GOOGLE_API_KEY=your_gemini_key
LLM_MODEL=gemini-2.5-flash
```

### 4️⃣ Run the app
```bash
streamlit run app.py
```

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first.

---

## 📬 Contact

If you have questions, feel free to reach out!

Email: pranaykale1506@gmail.com

GitHub: https://github.com/pranayk15
