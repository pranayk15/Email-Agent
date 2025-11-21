# new_email_agent.py
import smtplib
from email.mime.text import MIMEText
import os
import json
import re
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# ------------------------- LLM ---------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key="AIzaSyB5I_QHm08l-LrrCR6pQhputZr6GzwT9nw"
)

# ------------------------- STATE ----------------------------
class EmailState(dict):
    prompt: str
    recipient: str
    subject: str
    message: str
    status: str

    # NEW FIELDS FOR USER SMTP LOGIN
    smtp_email: str
    smtp_password: str
    smtp_server: str
    smtp_port: int


# ---------------------- NODE 1: PARSE PROMPT -----------------------
def parse_prompt(state: EmailState):
    prompt = state["prompt"]

    system_instruction = """
    You are an Email Extraction Agent.
    Extract the following:
      - recipient email(s)
      - subject
      - message

    Respond ONLY with pure JSON.
    Example:
    {
      "recipient": "abc@gmail.com",
      "subject": "Meeting Update",
      "message": "The meeting is at 5 PM."
    }
    """

    response = llm.invoke([
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt}
    ])

    raw = response.content.strip()
    print("\n===== RAW GEMINI OUTPUT =====")
    print(raw)
    print("================================\n")

    data = None

    # Try direct JSON
    try:
        data = json.loads(raw)
    except:
        pass

    # Try regex
    if data is None:
        try:
            json_match = re.search(r"\{.*\}", raw, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
        except:
            pass

    # Try markdown cleanup
    if data is None:
        try:
            cleaned = raw.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)
        except:
            pass

    if data is None:
        raise ValueError(f"Gemini did NOT return valid JSON!\nRaw output:\n{raw}")

    # Save to state
    state["recipient"] = data.get("recipient", "").strip()
    state["subject"] = data.get("subject", "").strip()
    state["message"] = data.get("message", "").strip()

    return state


# ---------------------- NODE 2: SEND EMAIL -----------------------
def send_email(state: EmailState):
    try:
        recipient = state["recipient"]
        subject = state["subject"]
        message = state["message"]

        smtp_email = state["smtp_email"]
        smtp_password = state["smtp_password"]
        smtp_server = state["smtp_server"]
        smtp_port = int(state["smtp_port"])

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = smtp_email
        msg["To"] = recipient

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, [recipient], msg.as_string())
        server.quit()

        state["status"] = f"Email sent successfully to {recipient}!"

    except Exception as e:
        state["status"] = f"Error: {e}"

    return state


# ------------------------- GRAPH ----------------------------
workflow = StateGraph(EmailState)

workflow.add_node("parse_prompt", parse_prompt)
workflow.add_node("send_email", send_email)

workflow.set_entry_point("parse_prompt")
workflow.add_edge("parse_prompt", "send_email")
workflow.add_edge("send_email", END)

email_graph = workflow.compile()

